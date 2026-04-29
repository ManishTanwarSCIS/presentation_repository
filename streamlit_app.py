from __future__ import annotations

import time
from pathlib import Path

import fitz
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
PDF_GLOB = "*.pdf"


def find_pdfs() -> list[Path]:
    return sorted(APP_DIR.glob(PDF_GLOB), key=lambda path: path.name.lower())


@st.cache_data(show_spinner=False)
def get_pdf_page_count(pdf_path: str, modified_time: float) -> int:
    del modified_time
    with fitz.open(pdf_path) as document:
        return document.page_count


@st.cache_data(show_spinner=False)
def render_page(pdf_path: str, modified_time: float, page_number: int, zoom: float) -> bytes:
    del modified_time
    with fitz.open(pdf_path) as document:
        page = document.load_page(page_number - 1)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        return pixmap.tobytes("png")


def reset_page_when_pdf_changes(pdf_name: str) -> None:
    if st.session_state.get("active_pdf") != pdf_name:
        st.session_state.active_pdf = pdf_name
        st.session_state.page_number = 1
        st.session_state.playing = False


def clamp_page(page_number: int, total_pages: int) -> int:
    return min(max(page_number, 1), total_pages)


def move_page(delta: int, total_pages: int) -> None:
    st.session_state.page_number = clamp_page(
        st.session_state.page_number + delta,
        total_pages,
    )


def main() -> None:
    st.set_page_config(
        page_title="PDF Slide Show",
        page_icon="slides",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 1.5rem;
            max-width: 1280px;
        }
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.85rem;
        }
        div[data-testid="stImage"] img {
            border: 1px solid rgba(49, 51, 63, 0.18);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
            background: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    pdfs = find_pdfs()
    if not pdfs:
        st.error(f"No PDF files found in {APP_DIR}.")
        st.stop()

    pdf_names = [pdf.name for pdf in pdfs]
    selected_name = st.sidebar.selectbox("PDF", pdf_names)
    selected_pdf = pdfs[pdf_names.index(selected_name)]
    reset_page_when_pdf_changes(selected_name)

    modified_time = selected_pdf.stat().st_mtime
    total_pages = get_pdf_page_count(str(selected_pdf), modified_time)
    st.session_state.page_number = clamp_page(
        st.session_state.get("page_number", 1),
        total_pages,
    )

    st.sidebar.header("Slide controls")
    st.session_state.page_number = st.sidebar.slider(
        "Slide",
        min_value=1,
        max_value=total_pages,
        value=st.session_state.page_number,
    )

    zoom = st.sidebar.slider(
        "Render quality",
        min_value=1.0,
        max_value=3.0,
        value=2.0,
        step=0.25,
    )

    interval = st.sidebar.slider(
        "Auto-play interval (seconds)",
        min_value=2,
        max_value=30,
        value=5,
    )

    previous_col, play_col, next_col = st.sidebar.columns(3)
    with previous_col:
        if st.button("Prev", use_container_width=True, disabled=st.session_state.page_number <= 1):
            move_page(-1, total_pages)
            st.rerun()
    with play_col:
        play_label = "Pause" if st.session_state.get("playing", False) else "Play"
        if st.button(play_label, use_container_width=True):
            st.session_state.playing = not st.session_state.get("playing", False)
            st.rerun()
    with next_col:
        if st.button("Next", use_container_width=True, disabled=st.session_state.page_number >= total_pages):
            move_page(1, total_pages)
            st.rerun()

    st.sidebar.caption(f"{selected_name} - {total_pages} slides")

    page_number = st.session_state.page_number
    st.title("PDF Slide Show")
    st.caption(f"{selected_name} | Slide {page_number} of {total_pages}")

    with st.spinner("Rendering slide..."):
        image = render_page(str(selected_pdf), modified_time, page_number, zoom)
    st.image(image, use_container_width=True)

    if st.session_state.get("playing", False):
        if st.session_state.page_number >= total_pages:
            st.session_state.playing = False
        else:
            time.sleep(interval)
            st.session_state.page_number += 1
        st.rerun()


if __name__ == "__main__":
    main()
