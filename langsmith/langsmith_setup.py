import os
from langsmith import Client
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "default"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"


client = Client()

llm = OpenAI(model_name="text-davinci-003")
prompt = "Write a poem about python and ai"
print(llm(prompt))
