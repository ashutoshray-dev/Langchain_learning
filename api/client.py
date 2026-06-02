import requests
import streamlit as st

def get_gemini_response(input_text):
    response=requests.post("http://localhost:4000/description/invoke",
    json={'input':{'product':input_text}})
    return response.json()['output']['content']

def get_gemma_response(input_text1):
    response=requests.post("http://localhost:4000/review/invoke",
    json={'input':{'product':input_text1}})
    return response.json()['output']

st.title('Langchain with API')
input_text = st.text_input("Write a description about")
input_text1 = st.text_input("Write a review about")

if input_text:
    st.write(get_gemini_response(input_text))

if input_text1:
    st.write(get_gemma_response(input_text1))

