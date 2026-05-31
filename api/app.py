from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn
import os
from langchain_ollama import OllamaLLM
from sse_starlette import EventSourceResponse
from dotenv import load_dotenv

load_dotenv()
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')
api_key=os.getenv('GEMINI_API_KEY')

app = FastAPI(
    title='Langchain Server',
    version='1.0',
    description='A simple API server'
)

add_routes(
    app,
    ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key),
    path = '/google-genai'
)
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=api_key)
llm = OllamaLLM(model = 'gemma3:1b')

prompt1 = ChatPromptTemplate.from_template('Write a description about {product} in 100 words')
prompt2 = ChatPromptTemplate.from_template('Write a review about {product} in 100 words.')

add_routes(
    app, 
    prompt1|model,
    path='/description'
)
add_routes(
    app, 
    prompt2|llm,
    path='/review'
)

if __name__ == '__main__':
    uvicorn.run(app,host='localhost',port=4000)
