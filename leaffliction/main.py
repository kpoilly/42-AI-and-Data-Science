import streamlit as st
import os


st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Welcome to Leaffliction! 👋")


def read_markdown_file():
    markdown_path = os.path.join(os.path.dirname(__file__), "readMe.md")
    with open(markdown_path, "r") as f:
        return f.read()


intro_markdown = read_markdown_file()
st.markdown(intro_markdown, unsafe_allow_html=True)
