
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, func, joinedload
import models
import schemas
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from schemas import SummaryResponse, SummaryRequest 
from langchain.prompts import PromptTemplate 
load_dotenv()
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=os.getenv("GROQ_API_KEY"),  # Correct usage!
    model_name="llama-3.3-70b-versatile"
)

app = FastAPI()
load_dotenv()

# Create tables if not exist
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    # Step 1: Create Movie
    db_movie = models.Movies(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)  

    # Step 2: Create related Actors using movie.id
    for actor in movie.actors:
        db_actor = models.Actors(**actor.model_dump(), movie_id=db_movie.id)
        db.add(db_actor)

    db.commit()
    db.refresh(db_movie)
    
    return db_movie

@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    result = (
        db.query(models.Movies)
        .options(joinedload(models.Movies.actors))
        .order_by(func.random())
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No movies found")
    return result

@app.post("/generate_summary/", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    
    movie = (
        db.query(models.Movies)
        .options(joinedload(models.Movies.actors))
        .filter(models.Movies.id == request.movie_id)
        .first()
    )

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Format actor list into a string like "Actor A, Actor B, and Actor C"
    actor_names = [actor.actor_name for actor in movie.actors]
    if len(actor_names) == 0:
        actor_list_str = "no known actors"
    elif len(actor_names) == 1:
        actor_list_str = actor_names[0]
    else:
        actor_list_str = ", ".join(actor_names[:-1]) + f", and {actor_names[-1]}"

    # Define prompt template
    prompt_template = PromptTemplate.from_template(
        "Generate a short, engaging summary for the movie '{title}' ({year}), directed by {director} and starring {actor_list}."
    )

    # Format prompt
    prompt = prompt_template.format(
        title=movie.title,
        year=movie.year,
        director=movie.director,
        actor_list=actor_list_str
    )

    # Invoke LLM
    try:
        summary = llm.invoke(prompt).content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")

    return SummaryResponse(summary_text=summary)

