# --------------------------------------------------------------
# Import libraries
# --------------------------------------------------------------

from dotenv import find_dotenv, load_dotenv
from langchain import OpenAI
from langchain.agents import (
    load_tools,
    initialize_agent,
    create_pandas_dataframe_agent,
    Tool,
    AgentType,
)

import pandas as pd


# --------------------------------------------------------------
# Load the OpenAI and Google Serp API tokens from the .env file
# --------------------------------------------------------------

load_dotenv(find_dotenv())

# --------------------------------------------------------------
# Use Serp API Tool to ask question
# --------------------------------------------------------------

llm = OpenAI(model="text-davinci-003", temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "what is the median salary of senior data scientists in 2023? what is the figure given there is a 10% increment?"
)


# --------------------------------------------------------------
# Load the dataset
# Download dataset at: https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023
# --------------------------------------------------------------

# Example with CSV
df = pd.read_csv("../data/ds_salaries.csv")

# Example with Excel
df = pd.read_excel("../data/ds_salaries.xlsx")

# --------------------------------------------------------------
# Initialize pandas dataframe agent
# --------------------------------------------------------------

agent = create_pandas_dataframe_agent(llm, df, verbose=True)


# --------------------------------------------------------------
# Perform basic data exploration
# --------------------------------------------------------------

agent.run("how many rows and columns are there in the dataset?")

agent.run("are there any missing values?")

agent.run("what are the columns?")

agent.run("how many categories are in each column?")


# --------------------------------------------------------------
# Perform multiple-steps data exploration
# --------------------------------------------------------------

agent.run("which are the top 5 jobs that have the highest median salary?")

agent.run("what is the percentage of data scientists who are working full time?")

agent.run("which company location has the most employees working remotely?")

agent.run("what is the most frequent job position for senior-level employees?")

agent.run(
    "what are the categories of company size? What is the proportion of employees they have? What is the total salary they pay for their employees?"
)
agent.run(
    "get median salaries of senior-level data scientists for each company size and plot them in a bar plot."
)

# --------------------------------------------------------------
# Initialize an agent with multiple dataframes
# --------------------------------------------------------------

df_2022 = df[df["work_year"] == 2022]
df_2023 = df[df["work_year"] == 2023]

agent = create_pandas_dataframe_agent(llm, [df_2022, df_2023], verbose=True)

# --------------------------------------------------------------
# Perform basic & multiple-steps data exploration for both dataframes
# --------------------------------------------------------------

agent.run("how many rows and columns are there for each dataframe?")

agent.run(
    "what are the differences in median salary for data scientists among the dataframes?"
)
agent.run(
    "how many people were hired for each of the dataframe? what are the percentages of experience levels?"
)
agent.run(
    "what is the median salary of senior data scientists for df2, given there is a 10% increment?"
)
