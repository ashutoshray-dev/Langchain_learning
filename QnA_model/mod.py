from langchain_ollama import OllamaLLM
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call, dynamic_prompt
from langchain.tools import tool
from dotenv import load_dotenv
from typing import TypedDict
from langchain.agents.structured_output import ProviderStrategy, ToolStrategy
from pydantic import BaseModel

load_dotenv()

# advanced_model = ChatOllama(
#     model='gemma3:1b',
#     temperature=0.7
# )
basic_model = ChatOllama(model='qwen2.5:3b', temperature=0.3)

# dyanmic model selection ---------------------------------------------
# @wrap_model_call
# def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
#     """Select model based on convesational complexity."""
#     message_count = len(request.state['messages'])
#     if message_count>20 :
#         model = advanced_model
#     else :
#         model = basic_model
#     return handler(request.override(model=model))

# @tool
# def get_weather_delhi() -> str:
#     "Get current weather condition of Delhi."
#     return "It's always sunny in delhi."
# @tool
# def get_weather_mumbai() -> str:
#     "Get current weather condition of Mumbai."
#     return f"It's always breezy here in mumbai."
# tools = [get_weather_delhi, get_weather_mumbai]
# basic_model_with_tools = basic_model.bind_tools(tools)

class Context(TypedDict):
    user_role: str

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are a helpful assistant."
    if user_role == 'expert':
        return f"{base_prompt} Provide technical responses."
    elif user_role == 'novice':
        return f"{base_prompt} Explain concepts like teaching to a 5-year old."

agent = create_agent(
    model=basic_model,    #default
    # system_prompt="You are a helpful assistant. Answer to all user queries in one response.To get Delhi's weather condition use tool get_weather_delhi()." \
    # "To get weather condition of Mumbai use tool get_weather_mumbai()",
    # tools=tools,
    # middleware=[dynamic_model_selection]
    middleware=[user_role_prompt],
    context_schema=Context,
    response_format= ToolStrategy(ContactInfo)
    # response_format=ProviderStrategy(ContactInfo)
)
query = "Extract contact info from the followig: Ashutosh, ashutosh@lang.com, 837466463"
response = agent.invoke(
    {'messages':[{'role':'user', 'content': query}]},
    context={"user_role": "novice"}
)
# for msg in response['messages']:
#     msg.pretty_print()

print(response['structured_response'])