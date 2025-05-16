

from database import Base, Column, Integer, String, ForeignKey, relationship

class Movies(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    actors = relationship("Actors", back_populates="movie")

class Actors(Base):
    __tablename__ = "actors"
    
    id = Column(Integer, primary_key=True)
    actor_name = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    movie = relationship("Movies", back_populates="actors")