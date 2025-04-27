import cv2
import streamlit as st
import numpy as np
import os
from predict import predict_from_file
from transformation import transformation_from_img
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


st.set_page_config(page_title="Prediction", page_icon="")

st.markdown("# Prediction")
st.sidebar.header("Prediction")
st.write(
    """This Page is used to predict the class of a leaf."""
)


def format_predictions_for_table(predictions_list):
    table_data = []
    for pred_dict in predictions_list:
        for model_name, (is_correct, class_name) in pred_dict.items():
            # Add checkmark or x emoji based on correctness
            status = "✅" if is_correct else "❌"
            # Create a row for the table
            table_data.append({
                "model_name": model_name,
                "OK": status,
                "class_predicted": class_name
            })
    return table_data


def view():
    imgFile = st.file_uploader(
        "image", type=["jpg", "jpeg", "JPG"])

    # Get the basename of the file if a file is uploaded
    if imgFile:
        file_basename = os.path.basename(imgFile.name)
        file_bytes = np.frombuffer(imgFile.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        images = transformation_from_img(img, st.pyplot)

        cols = st.columns(3)
        image_list = list(images.items())
        for i, (key, _img) in enumerate(image_list):
            with cols[i % 3]:
                st.image(_img, caption=key, use_container_width=True)

        if st.button("Predict"):
            with st.spinner("Predicting..."):
                models_name = ["original", "mask", "no_bg"]
                predictions, accuracy = predict_from_file(
                    img, file_basename,
                    models_name=models_name)
                st.success("Prediction completed!")
                table_data = format_predictions_for_table(predictions)
                st.write("### Prediction Results")
                st.table(table_data)


try:
    view()
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.stop()
