import streamlit as st
import re
from pathlib import Path

import yaml

REGEX_YAML_BLOCK = re.compile(r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r](.*)", re.DOTALL)


def render_preview(image, title, description):
    with st.container():
        image_col, text_col = st.columns((1,2))
        with image_col:
            st.image(image)

        with text_col:
            st.subheader(title)
            st.write(description)
            clicked = st.button("Read more...", key=title)
        return clicked


def render_page(post_path: Path):
    text = post_path.read_text()
    match = REGEX_YAML_BLOCK.search(text)
    page_content = match.group(2) if match else text
    st.markdown(page_content, unsafe_allow_html=True)


def get_page_data(post_path: Path):
    text = post_path.read_text()
    match = REGEX_YAML_BLOCK.search(text)
    if match:
        data = match.group(1)
        data = yaml.load(data, Loader=yaml.FullLoader)
        return data
    return {}


def main():
    st.set_page_config(layout="wide")
    posts = ['posts/hello_world.md', 'posts/check_this_out.md']
    page_to_show = None
    with st.sidebar:
    
        st.markdown('''
            <div align="center">
                <h1>A Test Blog!</h1>

            [![Github Badge](https://img.shields.io/github/stars/nateraw/host-a-blog-on-huggingface-spaces?style=social)](https://github.com/nateraw/host-a-blog-on-huggingface-spaces)
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('---')

        for post in posts:
            data = get_page_data(Path(post))
            clicked = render_preview(data.get("thumbnail"), data.get("title"), data.get("description"))
            if clicked:
                page_to_show = post

    if page_to_show:
        render_page(Path(page_to_show))

main()
