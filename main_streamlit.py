import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="🎬 Movie Explorer", layout="centered")
st.title("🎬 Movie Explorer")
st.markdown("Explore random movies and get AI-generated summaries")

# Initialize session state once
if "current_movie" not in st.session_state:
    st.session_state.current_movie = None

if "summary" not in st.session_state:
    st.session_state.summary = None

# Button to fetch random movie
if st.button("🎲 Show Random Movie", key="show_random_movie"):
    with st.spinner("Fetching a random movie..."):
        try:
            response = requests.get("http://localhost:8000/movies/random/")
            if response.status_code == 200:
                # Save current movie and clear any old summary
                st.session_state.current_movie = response.json()
                st.session_state.summary = None
            else:
                st.error("Failed to load movie. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")

# Display movie details if available
if st.session_state.current_movie:
    movie = st.session_state.current_movie
    st.header(movie["title"])
    st.write(f"**Year:** {movie['year']}")
    st.write(f"**Director:** {movie['director']}")

    st.subheader("🎭 Actors")
    for actor in movie["actors"]:
        st.write(f"- {actor['actor_name']}")

    # Button to generate summary
    if st.button("📝 Get Summary", key="get_summary_button"):
        with st.spinner("Generating summary..."):
            try:
                payload = {"movie_id": movie["id"]}
                response = requests.post("http://localhost:8000/generate_summary/", json=payload)
                if response.status_code == 200:
                    st.session_state.summary = response.json()["summary_text"]
                else:
                    st.error("Failed to generate summary.")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")

    # Display summary if available
    if st.session_state.summary:
        st.subheader("🔍 Summary")
        st.info(st.session_state.summary)
else:
    st.info("Click 'Show Random Movie' to begin exploring.")