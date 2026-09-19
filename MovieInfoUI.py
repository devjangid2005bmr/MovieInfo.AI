import json
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from pydantic import BaseModel
from typing import Optional, List


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="DEVV.AI — Movie Extractor",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_dotenv()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(120, 80, 255, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(0, 210, 255, 0.08),
                transparent 30%
            ),
            #08090d;
        color: #f5f5f7;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ---------- HEADER ---------- */

    .devv-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 0 28px 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 45px;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .brand span {
        color: #8b7cff;
    }

    .status {
        padding: 7px 13px;
        border-radius: 100px;
        background: rgba(72, 214, 128, 0.10);
        border: 1px solid rgba(72, 214, 128, 0.20);
        color: #63e69b;
        font-size: 12px;
        font-weight: 600;
    }

    /* ---------- HERO ---------- */

    .hero {
        text-align: center;
        margin-bottom: 40px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 100px;
        background: rgba(139,124,255,0.10);
        border: 1px solid rgba(139,124,255,0.20);
        color: #a99fff;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: 52px;
        line-height: 1.05;
        letter-spacing: -2.5px;
        margin: 0;
        font-weight: 800;
    }

    .hero h1 span {
        background: linear-gradient(
            90deg,
            #9d8cff,
            #63d9ff
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #92949e;
        font-size: 17px;
        max-width: 650px;
        margin: 18px auto 0 auto;
        line-height: 1.6;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 14px;
        font-weight: 700;
        color: #d7d7dc;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
    }

    /* ---------- TEXT AREA ---------- */

    textarea {
        background: #101116 !important;
        color: #eeeeef !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 16px !important;
        padding: 16px !important;
    }

    textarea:focus {
        border-color: rgba(139,124,255,0.55) !important;
        box-shadow: 0 0 0 1px rgba(139,124,255,0.20) !important;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%;
        height: 48px;
        border-radius: 12px;
        border: 0;
        background: linear-gradient(
            90deg,
            #7564ff,
            #8d7cff
        );
        color: white;
        font-weight: 700;
        font-size: 14px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 25px rgba(117,100,255,0.25);
    }

    /* ---------- MOVIE CARD ---------- */

    .movie-card {
        background: rgba(17,18,24,0.85);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px;
        margin-top: 25px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.20);
    }

    .movie-title {
        font-size: 31px;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }

    .movie-meta {
        color: #8e9099;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .info-label {
        color: #777984;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .info-value {
        color: #eeeeef;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .genre {
        display: inline-block;
        padding: 6px 10px;
        margin: 3px;
        border-radius: 8px;
        background: rgba(139,124,255,0.10);
        border: 1px solid rgba(139,124,255,0.18);
        color: #b3aaff;
        font-size: 12px;
    }

    .cast-item {
        padding: 8px 0;
        color: #d7d7dc;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .summary {
        color: #b5b6be;
        line-height: 1.7;
        font-size: 14px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #555762;
        font-size: 12px;
        margin-top: 70px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.06);
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# MODEL
# =========================================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# =========================================================
# PYDANTIC MODEL
# =========================================================

class Movie(BaseModel):
    title: str
    release_year: int
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str


# =========================================================
# PARSER
# =========================================================

parser = PydanticOutputParser(
    pydantic_object=Movie
)


# =========================================================
# PROMPT
# =========================================================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Extract movie information from the paragraph.

        {format_instruction}
        """
    ),
    (
        "human",
        "{paragraph}"
    )
])


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="devv-header">
    <div class="brand">✦ DEVV<span>.AI</span></div>
    <div class="status">● AI ONLINE</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        ✦ POWERED BY GEMINI + PYDANTIC
    </div>

    <h1>
        Turn movie text into
        <span>structured data.</span>
    </h1>

    <p>
        Paste any movie description, article or paragraph.
        DEVV.AI extracts the important movie information
        into a clean structured format automatically.
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT
# =========================================================

st.markdown(
    '<div class="section-title">MOVIE DESCRIPTION</div>',
    unsafe_allow_html=True
)

paragraph = st.text_area(
    "",
    placeholder=(
        "Paste a movie paragraph here...\n\n"
        "Example: Dhurandhar is a 2025 spy action thriller "
        "directed by Aditya Dhar..."
    ),
    height=190,
    label_visibility="collapsed"
)


# =========================================================
# EXTRACT BUTTON
# =========================================================

extract = st.button(
    "✦  Extract Movie Information",
    use_container_width=True
)


# =========================================================
# PROCESS
# =========================================================

if extract:

    if not paragraph.strip():

        st.warning("Please enter a movie paragraph first.")

    else:

        with st.spinner("DEVV.AI is extracting movie information..."):

            try:

                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instruction":
                        parser.get_format_instructions()
                })

                response = model.invoke(final_prompt)

                # Gemini structured content → text
                if isinstance(response.content, list):

                    text = "".join(
                        block.get("text", "")
                        for block in response.content
                        if isinstance(block, dict)
                    )

                else:

                    text = response.content

                # Parse with Pydantic
                result = parser.parse(text)

                # Save result
                st.session_state["movie_result"] = result

            except Exception as e:

                st.error(
                    f"Something went wrong while extracting data:\n\n{e}"
                )


# =========================================================
# RESULT
# =========================================================

if "movie_result" in st.session_state:

    movie = st.session_state["movie_result"]

    st.markdown(
        '<div class="section-title">EXTRACTED INFORMATION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="movie-card">

            <div class="movie-title">
                {movie.title}
            </div>

            <div class="movie-meta">
                {movie.release_year}
                &nbsp; • &nbsp;
                {movie.director or "Unknown Director"}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # Basic information
    # -----------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="info-label">RELEASE YEAR</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="info-value">{movie.release_year}</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="info-label">DIRECTOR</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="info-value">{movie.director or "Unknown"}</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            '<div class="info-label">RATING</div>',
            unsafe_allow_html=True
        )

        rating = (
            f"⭐ {movie.rating}"
            if movie.rating is not None
            else "Not available"
        )

        st.markdown(
            f'<div class="info-value">{rating}</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------
    # Genre
    # -----------------------------------------

    st.markdown(
        '<div class="info-label">GENRE</div>',
        unsafe_allow_html=True
    )

    genres = "".join(
        f'<span class="genre">{genre}</span>'
        for genre in movie.genre
    )

    st.markdown(
        genres,
        unsafe_allow_html=True
    )


    st.write("")


    # -----------------------------------------
    # Cast + Summary
    # -----------------------------------------

    left, right = st.columns([1, 1.5])

    with left:

        st.markdown(
            '<div class="info-label">CAST</div>',
            unsafe_allow_html=True
        )

        for actor in movie.cast:

            st.markdown(
                f'<div class="cast-item">• {actor}</div>',
                unsafe_allow_html=True
            )


    with right:

        st.markdown(
            '<div class="info-label">SUMMARY</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="summary">{movie.summary}</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------
    # JSON
    # -----------------------------------------

    st.write("")

    with st.expander("View structured JSON"):

        movie_json = movie.model_dump()

        st.json(movie_json)

        st.download_button(
            label="↓ Download JSON",
            data=json.dumps(
                movie_json,
                indent=4,
                ensure_ascii=False
            ),
            file_name="movie_data.json",
            mime="application/json"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    ✦ DEVV.AI &nbsp; • &nbsp;
    Intelligent Data Extraction
</div>
""", unsafe_allow_html=True)