# Extract Structured Information From LLM Outputs Using OpenAI's Function Calling Feature

This repository contains an implementation of OpenAI's function calling feature. We compare the outputs of ChatGPT, with and without function calling. 
Based on a given prompt, the function calling feature not only returns the most relevant function to be used, it also pre-fills the arguments needed for the function.
The use case is also implemented in Langchain ChatModel in a multiple requests setting.

## What is OpenAI's Function Calling Capability?

ChatGPT has conversational features, but sometimes its flexibility results in incoherent outputs. As developers, we prefer to have deterministic and reliable responses. 

With the new function calling feature from OpenAI, developers can supply a given LLM a list of tools and customized functions. Instead of replying with natural language, the model will return the most relevant function based on the user prompt, together with prefilled arguments as a JSON object.​[^1]

The feature currently works on the `gpt-4-0613` and `gpt-3.5-turbo-0613` models. 

## Why Is This a Huge Update?

This feature basically opens up endless possibilities for LLM applications.

-	ChatGPT returns natural text, and it can be unreliable. Returning functions makes the output more controlled and deterministic.
-	The feature can extract structured data from text (prompt) and assign them as arguments to a chosen function.
-	Developers can create their own functions connecting the LLMs to internal and external APIs and databases, and let the model decides which function to use and which arguments to pass.
-	Non-technical users can interact with LLMs to obtain data without having to know the underlying functions and required arguments.

## Basic Example of How to Use OpenAI Functions 

<b>Use case (Part 1)</b>: Chat models with and without function calling (gpt-3.5-turbo and gpt-4)
-	We ask the model a question about a particular flight information. 
-	Without function calling, the chat model responded that it does not have flight information.
-	With function calling, the chat model obtains the information from a given function and returns an answer.

## Example of How to Use These Functions to Control the Flow of a Chatbot

<b>Use case (Part 2)</b>: Airport customer service scenario
-	Single prompt and function
-	Multiple prompts and functions
-	Conversational chatbot with Langchain

Observations from the use cases: 
-	Function calling not only chooses the most relevant function based on given prompt, but it also auto-fills the required arguments.
-	The feature only returns the function and arguments, it does not run the function, but we can do this manually in our code.
-	We can streamline the function implementation using the `json.loads()` and `eval()` methods.
-   By feeding the output of the function call back into the messages, we can get a natural language response.

Possible extension of the use cases:
-	Use the OpenAI_FUNCTIONS agent​[^2] in Langchain to execute customized functions as tools.
-	To replace the hard-coded functions to retrieve information from API calls and/or database queries.
-	Utilize existing tools to do text generation, image generation, translation, and more.
-	Explore multiple-steps operations, such as a real-life ticket booking transaction (search, update db, payment, print tickets).

## Setting Up the Experiment
You can find the code for setting up and running the experiment in the `openai_function_calling.py` file in this repository. 
Note: Make sure your device has Python 3.9 or higher and an up-to-date version of Langchain module to execute the scripts successfully.

Below is a brief description of the key steps in the code:

1. Load the OpenAI token from the .env file.
2. Execute use case 1: 
    -	Ask ChatGPT a question regarding flight information.
    -	Implement function calling, compare outcome.
    - 	Implement a hard-coded function, compare outcome.
3. Execute use case 2: 
    -	Implement 3 functions and test them with different prompts. 
    -	Implement conversational chat model with Langchain with the functions and test it with a prompt with several requests.


[^1]: https://openai.com/blog/function-calling-and-other-api-updates
[^2]: https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent
