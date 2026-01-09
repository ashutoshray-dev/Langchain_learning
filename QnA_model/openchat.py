from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGSMITH_TRACING"] = 'true'

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpful assistant. Please respond to the queries.'),
        ('user', 'Query:{Query}')
    ]
)
# messages = [
#         ('system', 'You are a helpful assistant. Please respond to the queries.'),
#         ('user', 'What are transformers?')
#     ]
st.title('Langchain with Ollama:Gemma3-1b')
input_text = st.text_input('Search the topic u want')
# input_text = input('Enter your input: ')

llm = OllamaLLM(model='gemma3:1b')
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'Query':input_text})) 
# response = llm.invoke(messages)
# print(response)