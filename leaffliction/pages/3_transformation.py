import streamlit as st
from transformation import transformation_from_img
import cv2
import numpy as np

st.set_page_config(page_title="Transformation", page_icon="")

st.markdown("# Transformation")
st.sidebar.header("Transformation")
st.write(
    """This Page is used to visualize the transformation process."""
)


def view():
    imgFile = st.file_uploader(
        "image", type=["jpg", "jpeg", "JPG"])

    if imgFile:
        st.write("### Original image")
        st.image(imgFile, caption="Original Image", use_container_width=True)

        if st.button("Show transformed images"):
            with st.spinner("Generating transformed images..."):
                file_bytes = np.frombuffer(imgFile.read(), np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                images = transformation_from_img(
                    img, st.pyplot)
                st.success("Images generated!")

                for key, img in images.items():
                    st.write(key)
                    st.image(img, caption=key, use_container_width=True)


view()
