from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
# os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
# os.environ['LANGCHAIN_TRACING_V2'] = 'true'
# os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google api key not found")
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpful assistant. Please respond to user queries.'),
        ('user', 'Query:{Query}')
    ]
)

st.title('Langchain with Gemini')
input_text = st.text_input('Search the topic u want')

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'Query': input_text}))