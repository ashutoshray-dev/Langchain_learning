from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

messages = [
        ('system', 'You are a helpful assistant. Please respond to the queries.'),
        ('user', 'What are transformers?')
    ]

llm = OllamaLLM(model='gemma3:1b')
response = llm.invoke(messages)
print(response)