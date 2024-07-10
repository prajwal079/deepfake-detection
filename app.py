import streamlit as st
from keras.models import model_from_json
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
from pathlib import Path
import os

st.set_page_config(page_title="Deepfake Detection")

model_index = "_"
f = Path(f"models/model_structure{model_index}.json")  
model_structure = f.read_text()
model = model_from_json(model_structure)
model.load_weights(f"models/model_weights{model_index}.h5")  


def convert_to_ela_image(image_path, quality):
    temp_filename = 'temp_file_name.jpg'
    ela_filename = 'temp_ela.png'
    
    image = Image.open(image_path).convert('RGB')
    image.save(temp_filename, 'JPEG', quality=quality)
    temp_image = Image.open(temp_filename)
    
    ela_image = ImageChops.difference(image, temp_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return ela_image


st.title("Deepfake detection")

st.markdown(
    """
    <style>
    .st-emotion-cache-16txtl3 { padding-top: 0px !important; }
    .eczjsme4 { padding-top: 20px !important; }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.header("About")
st.sidebar.info(
    "This application is designed to detect deepfake images using ELA + ML. "
    "Upload an image and the system will analyze it to determine if it's real or a deepfake."
)

uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    
    ela_image = convert_to_ela_image(uploaded_file, 90)
    with st.expander("ELA Image"):
        st.image(ela_image, use_column_width=True) 
    ela_image_resized = ela_image.resize((128, 128))
    img_array = np.array(ela_image_resized).flatten() / 255.0
    img_array = img_array.reshape((-1, 128, 128, 3))
    
    prediction = model.predict(img_array)
    class_names = {0: 'Fake', 1: 'Real'}
    
    most_likely_class_index = int(np.argmax(prediction))
    if np.max(prediction) < 0.84:
        if most_likely_class_index == 1:
            most_likely_class_index = 1 - most_likely_class_index
    class_label = class_names[most_likely_class_index]
    class_likelihood = prediction[0][most_likely_class_index]
    
    
    st.markdown(f"<span style='font-size: 24px;'>Predicted class is  {class_label} <br /> Confidence Score: {class_likelihood:.2f}</span>", unsafe_allow_html=True)
