# Exploratory Data Analysis With Pandas Dataframe Agent

This repository contains the script for performing exploratory data analysis using Pandas Dataframe Agent from Langchain. Instead of manually doing EDA, the agent takes a prompt, 
decides on the code to do data analysis, and returns the answer. The use case also includes EDA for multiple dataframes. 

What you need to follow this tutotial:
1. Understand how Python works
2. Understand how LangChain works
3. OpenAI API key (GPT4 is not required)


## What Are LangChain Agents?

Agents use an LLM to determine which actions to take and in what order. They can have access to a series of tools and can decide which ones to call according to given user input (prompt)​[^1].

Text in, text out. Prompt in, answer out. 

There are two types of agents: 
1. action agents and 
2. plan-and-execute agents

- Action agents are more straightforward, executing one action at a time.
- Plan-and-execute agents first plans what actions to take, and then execute them one at a time.
- For small tasks, use action agents.
- For longer tasks, use plan-and-execute agents to maintain objective and focus, and then execute using action agents.

High-level pseudocode of an Action Agent:
-	The user gives a prompt and lists available tools
-	The agent decides which tool to use based on the prompt
-	A tool is called, return output to agent
-	The agent decides the next step to take
-	Stops iteration when the agent has enough information. Responds to the user with an answer

High-level pseudocode of a Plan-and-Execute Agent:
-	The user gives a prompt and lists available tools
-	The planner lists out the steps to take
-	The executor goes through the steps and execute action one by one 


## What Are the Different Types of Agents?

Agent types available in LangChain[^2]:

1. zero-shot-react-description
    - This agent uses the ReAct framework to determine which tool to use based solely on the <b>tool’s description</b>. 
    - Must include tool description.
    - Most examples use this agent type.

    What is the ReAct framework?[^3] 
    - Synergize <b>reasoning</b> and <b>acting</b> in language models.
    - Reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while 
    actions allow it to interface with and gather additional information from external sources such as knowledge 
    bases or environments.

    Example: https://python.langchain.com/en/latest/modules/agents/getting_started.html

2. react-docstore
    - This agent uses the ReAct framework to interact with a <b>docstore</b>.
    - Must include a Search tool (search for a document), and a Lookup tool (look for a term in found document).

    What is a docstore?[^4]
    - It can be 1) a document in the form of dictionary loaded in-memory, or 2) the Wikipedia API.

    Example: https://python.langchain.com/en/latest/modules/agents/agents/examples/react.html

3. self-ask-with-search
    - This agent utilizes a single tool that should be named Intermediate Answer. This tool should be able to lookup <b>factual answers</b> to questions.
    - Uses Google search API as the tool.

    - What is the self-ask model?[^5]
    The model explicitly asks itself (and then answers) follow-up questions before answering the initial question.

    Example: https://python.langchain.com/en/latest/modules/agents/agents/examples/self_ask_with_search.html

4. conversational-react-description
    - It uses the ReAct framework to decide which tool to use and uses memory to remember the previous <b>conversation</b> interactions. 
    - The prompt is designed to make the agent helpful and conversational.

    Example: https://python.langchain.com/en/latest/modules/agents/agents/examples/conversational_agent.html


## What Are Tools?

Tools are ways that an agent can use to interact with the outside world[^6].

Tools categorized by usage:
-	Data access: ArXiv, PubMed, Wikipedia, Google Places, OpenWeatherMap
-	Web search: Bing, Brave, DuckDuckGo, Google, Google Serper API, Metaphor Search, SearxNG, Serp API, YouTube
-	LLMs & ML functions: ChatGPT, Gradio, HuggingFace 
-	Automation: Apify, AWS Lambda API, Shell, File System, IFTTT WebHooks, Python REPL, Twilio, Zapier, GraphQL, Requests, SceneXplain, Wolfram Alpha
-	Special: Human as a tool

<b>Use case (Part 1)</b>: Use the serpapi[^7] tool to ask a question, and the llm-math tool for calculation (with zero shot agent type).


## What Are Toolkits?

Toolkits are groups of tools designed for a specific use case[^8]. For example, for an agent to interact with a SQL database in the best way it may need access to one tool to execute queries and another tool to inspect tables.

Pandas Dataframe Agent[^10]: an agent used to interact with a pandas dataframe. It is mostly optimized for question answering.
This agent calls the Python agent under the hood, which executes LLM generated Python code.

It can be used for a single dataframe or for multiple dataframes, for usage like:
- Question and answers as part of exploratory data analysis
- Compare differences between two dataframes

<b>Use case (Part 2)</b>: Exploratory data analysis with data science salaries dataset
-	Dataset: Salaries of different data science fields from 2020 to 2023[^11]
-	Basic data exploration (shape, isnull, columns, nunique)
-	Multiple-steps data exploration (sort, slice, filter, multiple-step calculations, groupby)
-	Multiple dataframes (comparison, multiple-step calculations)


Observations from the use case: 
-	The pandas dataframe agent is useful for data exploration, where it is only Q&A involved. It is not ready for data manipulation or any action that changes the dataframe. The agent managed to come up with the code to manipulate data, but it does not apply the changes. For example, actions like replace values, create new dataframe or save plots do not work, so better do that manually.
-	It is useful to double check the answers manually. Two incorrect answers found and demonstrated in the use case. You might get a different outcome than mine.
-	The agent can recognize data values based on context without explicit description. Such as: FT = Full-time, job_title = job designation.
-	It does not remember the conversation as much. When there are more than 2 steps in a prompt, it does not handle it perfectly, something might slip through the cracks.
-	One can save time in data manipulation by prompting the code and applying that manually, instead of looking up for the code from Google search or documentation.

Possible extension of the use case: to train a neural net using the Python Agent Toolkit.


## Setting Up the Experiment

You can find the code for setting up and running the experiment in the `pandas_agent.py` file in this repository. 
Note: You'll need Python 3.9 or higher and an up-to-date version of Langchain package to use the `create_pandas_dataframe_agent` function.

Below is a brief description of the key steps in the code:

1. Load the OpenAI and Serp API tokens from the .env file.
2. Execute use case 1: ask a question with the serp api and llm-math tools.
3. Execute use case 2: 
    - Execute basic data exploration (shape, isnull, columns, nunique)
    - Execute multiple-steps data exploration (sort, slice, filter, multiple-step calculations, groupby)
    - Compare multiple dataframes (comparison, multiple-step calculations)
8. Compare the output from Step 2 and Step 3.


[^1]: https://python.langchain.com/docs/modules/agents/
[^2]: https://python.langchain.com/docs/modules/agents/agent_types/
[^3]: https://arxiv.org/pdf/2210.03629.pdf
[^4]: https://python.langchain.com/docs/modules/data_connection/
[^5]: https://ofir.io/self-ask.pdf
[^6]: https://python.langchain.com/docs/modules/agents/tools/
[^7]: https://python.langchain.com/docs/modules/agents/agent_types/self_ask_with_search
[^8]: https://python.langchain.com/docs/modules/agents/
[^9]: https://python.langchain.com/docs/modules/agents/toolkits/
[^10]: https://python.langchain.com/docs/modules/agents/toolkits/pandas
[^11]: https://www.kaggle.com/datasets/arnabchaki/data-science-salaries-2023