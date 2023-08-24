from dotenv import find_dotenv, load_dotenv
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents.load_tools import get_all_tool_names
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI

# Load environment variables
load_dotenv(find_dotenv())

# --------------------------------------------------------------
# LLMs: Get predictions from a language model
# --------------------------------------------------------------

llm = OpenAI(model_name="text-davinci-003")
prompt = "Write a poem about python and ai"
print(llm(prompt))


# --------------------------------------------------------------
# Prompt Templates: Manage prompts for LLMs
# --------------------------------------------------------------

prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

prompt.format(product="Smart Apps using Large Language Models (LLMs)")

# --------------------------------------------------------------
# Chains: Combine LLMs and prompts in multi-step workflows
# --------------------------------------------------------------

llm = OpenAI()
prompt = PromptTemplate(
    input_variables=["product"],
    template="What is a good name for a company that makes {product}?",
)

chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run("AI Chatbots for Dental Offices"))

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write an email subject for this topic {topic}?",
)

chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run("AI Session"))

# --------------------------------------------------------------
# Agents: Dynamically Call Chains Based on User Input
# --------------------------------------------------------------


llm = OpenAI()

get_all_tool_names()
tools = load_tools(["wikipedia", "llm-math"], llm=llm)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Now let's test it out!
result = agent.run(
    "In what year was python released and who is the original creator? Multiply the year by 3"
)
print(result)

# Now let's test it out!
result = agent.run(
    "In what year was Tesla released and who is the original creator? Multiply the year by 3"
)
print(result)

# Now let's test it out!
result = agent.run(
    "In what year was Tesla born? and who is the original creator? Multiply the year by 3"
)
print(result)


# --------------------------------------------------------------
# Memory: Add State to Chains and Agents
# --------------------------------------------------------------

llm = OpenAI()
conversation = ConversationChain(llm=llm, verbose=True)

output = conversation.predict(input="Hi there!")
print(output)

output = conversation.predict(
    input="I'm doing well! Just having a conversation with an AI."
)
print(output)

# --------------------------------------------------------------
# Chatmodels: Create Conversational Agents
# --------------------------------------------------------------

llm = OpenAI()
chat_model = ChatOpenAI()
