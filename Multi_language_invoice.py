from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load Gemini Pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_model_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#intialize our streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")
input = st.text_input("Input prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)
submit = st.button("Tell me about invoice") 

input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice and
you will have to answer any questions based on the uploaded invoices image
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_model_response(input_prompt,image_data,image)
    st.subheader("The Response is")
    st.write(response)
