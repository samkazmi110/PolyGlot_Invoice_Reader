import streamlit as st
from dotenv import load_dotenv
import os


load_dotenv() ## load all environment variable from .env file

from PIL import Image
import google.generativeai  as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## function to load gemeni pro vision
## available models
_=""" models/gemini-1.0-pro
models/gemini-1.0-pro-001
models/gemini-1.0-pro-latest
models/gemini-1.0-pro-vision-latest
models/gemini-1.5-pro-latest
models/gemini-pro
models/gemini-pro-vision """

def get_gemini_response(input,image, prompt):
        model=genai.GenerativeModel(model_name="gemini-pro-vision")
        response = model.generate_content([input,image[0],prompt])
        return response.text

def input_image_setup(uploaded_file):

    if uploaded_file is not None:
    # read the file into bytes
        image_bytes = uploaded_file.getvalue()
        image_parts =[
            {
            "mime_type":uploaded_file.type,
            "data":image_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
## initialize streamlit app

st.set_page_config(page_title="PolyGlot Invoice Reader: ",page_icon=":books:")
st.header("Harnessing Google Gemini Pro API for Multilingual Data Extraction")
input = st.text_input("Input Prompt:", key="input")

uploaded_file = st.file_uploader("Upload Image of invoice:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    
subtmit = st.button("Extract Information from invoice")


input_prompt = """
You are an expert in understanding invoices. we will upload a image of an invoice and you will provide a summary of the invoice.
and you will have to answer any question based on the uploaded invoice image
"""
##if submit is clicked
if subtmit:
    image_data=input_image_setup(uploaded_file)

    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is: ")
    st.write(response)
