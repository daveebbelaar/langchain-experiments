# --------------------------------------------------------------
# Import Modules
# --------------------------------------------------------------

import os
import json
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage


# --------------------------------------------------------------
# Load OpenAI API Token From the .env File
# --------------------------------------------------------------

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# --------------------------------------------------------------
# Ask ChatGPT a Question
# --------------------------------------------------------------

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": "When's the next flight from Amsterdam to New York?",
        },
    ],
)

output = completion.choices[0].message.content
print(output)

# --------------------------------------------------------------
# Use OpenAI’s Function Calling Feature
# --------------------------------------------------------------

function_descriptions = [
    {
        "name": "get_flight_info",
        "description": "Get flight information between two locations",
        "parameters": {
            "type": "object",
            "properties": {
                "loc_origin": {
                    "type": "string",
                    "description": "The departure airport, e.g. DUS",
                },
                "loc_destination": {
                    "type": "string",
                    "description": "The destination airport, e.g. HAM",
                },
            },
            "required": ["loc_origin", "loc_destination"],
        },
    }
]

user_prompt = "When's the next flight from Amsterdam to New York?"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": user_prompt}],
    # Add function calling
    functions=function_descriptions,
    function_call="auto",  # specify the function call
)

# It automatically fills the arguments with correct info based on the prompt
# Note: the function does not exist yet

output = completion.choices[0].message
print(output)

# --------------------------------------------------------------
# Add a Function
# --------------------------------------------------------------


def get_flight_info(loc_origin, loc_destination):
    """Get flight information between two locations."""

    # Example output returned from an API or database
    flight_info = {
        "loc_origin": loc_origin,
        "loc_destination": loc_destination,
        "datetime": str(datetime.now() + timedelta(hours=2)),
        "airline": "KLM",
        "flight": "KL643",
    }

    return json.dumps(flight_info)


# Use the LLM output to manually call the function
# The json.loads function converts the string to a Python object

origin = json.loads(output.function_call.arguments).get("loc_origin")
destination = json.loads(output.function_call.arguments).get("loc_destination")
params = json.loads(output.function_call.arguments)
type(params)

print(origin)
print(destination)
print(params)

# Call the function with arguments

chosen_function = eval(output.function_call.name)
flight = chosen_function(**params)

print(flight)

# --------------------------------------------------------------
# Add function result to the prompt for a final answer
# --------------------------------------------------------------

# The key is to add the function output back to the messages with role: function
second_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "user", "content": user_prompt},
        {"role": "function", "name": output.function_call.name, "content": flight},
    ],
    functions=function_descriptions,
)
response = second_completion.choices[0].message.content
print(response)

# --------------------------------------------------------------
# Include Multiple Functions
# --------------------------------------------------------------

# Expand on function descriptions (3 functions)

function_descriptions_multiple = [
    {
        "name": "get_flight_info",
        "description": "Get flight information between two locations",
        "parameters": {
            "type": "object",
            "properties": {
                "loc_origin": {
                    "type": "string",
                    "description": "The departure airport, e.g. DUS",
                },
                "loc_destination": {
                    "type": "string",
                    "description": "The destination airport, e.g. HAM",
                },
            },
            "required": ["loc_origin", "loc_destination"],
        },
    },
    {
        "name": "book_flight",
        "description": "Book a flight based on flight information",
        "parameters": {
            "type": "object",
            "properties": {
                "loc_origin": {
                    "type": "string",
                    "description": "The departure airport, e.g. DUS",
                },
                "loc_destination": {
                    "type": "string",
                    "description": "The destination airport, e.g. HAM",
                },
                "datetime": {
                    "type": "string",
                    "description": "The date and time of the flight, e.g. 2023-01-01 01:01",
                },
                "airline": {
                    "type": "string",
                    "description": "The service airline, e.g. Lufthansa",
                },
            },
            "required": ["loc_origin", "loc_destination", "datetime", "airline"],
        },
    },
    {
        "name": "file_complaint",
        "description": "File a complaint as a customer",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the user, e.g. John Doe",
                },
                "email": {
                    "type": "string",
                    "description": "The email address of the user, e.g. john@doe.com",
                },
                "text": {
                    "type": "string",
                    "description": "Description of issue",
                },
            },
            "required": ["name", "email", "text"],
        },
    },
]

print(function_descriptions_multiple)


def ask_and_reply(prompt):
    """Give LLM a given prompt and get an answer."""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": prompt}],
        # add function calling
        functions=function_descriptions_multiple,
        function_call="auto",  # specify the function call
    )

    output = completion.choices[0].message
    return output


# Scenario 1: Check flight details

user_prompt = "When's the next flight from Amsterdam to New York?"
print(ask_and_reply(user_prompt))

# Get info for the next prompt

origin = json.loads(output.function_call.arguments).get("loc_origin")
destination = json.loads(output.function_call.arguments).get("loc_destination")
chosen_function = eval(output.function_call.name)
flight = chosen_function(origin, destination)

print(origin)
print(destination)
print(flight)

flight_datetime = json.loads(flight).get("datetime")
flight_airline = json.loads(flight).get("airline")

print(flight_datetime)
print(flight_airline)

# Scenario 2: Book a new flight

user_prompt = f"I want to book a flight from {origin} to {destination} on {flight_datetime} with {flight_airline}"
print(ask_and_reply(user_prompt))

# Scenario 3: File a complaint

user_prompt = "This is John Doe. I want to file a complaint about my missed flight. It was an unpleasant surprise. Email me a copy of the complaint to john@doe.com."
print(ask_and_reply(user_prompt))

# --------------------------------------------------------------
# Make It Conversational With Langchain
# --------------------------------------------------------------

llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)

# Start a conversation with multiple requests

user_prompt = """
This is Jane Harris. I am an unhappy customer that wants you to do several things.
First, I neeed to know when's the next flight from Amsterdam to New York.
Please proceed to book that flight for me.
Also, I want to file a complaint about my missed flight. It was an unpleasant surprise. 
Email me a copy of the complaint to jane@harris.com.
Please give me a confirmation after all of these are done.
"""

# Returns the function of the first request (get_flight_info)

first_response = llm.predict_messages(
    [HumanMessage(content=user_prompt)], functions=function_descriptions_multiple
)

print(first_response)

# Returns the function of the second request (book_flight)
# It takes all the arguments from the prompt but not the returned information

second_response = llm.predict_messages(
    [
        HumanMessage(content=user_prompt),
        AIMessage(content=str(first_response.additional_kwargs)),
        AIMessage(
            role="function",
            additional_kwargs={
                "name": first_response.additional_kwargs["function_call"]["name"]
            },
            content=f"Completed function {first_response.additional_kwargs['function_call']['name']}",
        ),
    ],
    functions=function_descriptions_multiple,
)

print(second_response)

# Returns the function of the third request (file_complaint)

third_response = llm.predict_messages(
    [
        HumanMessage(content=user_prompt),
        AIMessage(content=str(first_response.additional_kwargs)),
        AIMessage(content=str(second_response.additional_kwargs)),
        AIMessage(
            role="function",
            additional_kwargs={
                "name": second_response.additional_kwargs["function_call"]["name"]
            },
            content=f"Completed function {second_response.additional_kwargs['function_call']['name']}",
        ),
    ],
    functions=function_descriptions_multiple,
)

print(third_response)

# Conversational reply at the end of requests

fourth_response = llm.predict_messages(
    [
        HumanMessage(content=user_prompt),
        AIMessage(content=str(first_response.additional_kwargs)),
        AIMessage(content=str(second_response.additional_kwargs)),
        AIMessage(content=str(third_response.additional_kwargs)),
        AIMessage(
            role="function",
            additional_kwargs={
                "name": third_response.additional_kwargs["function_call"]["name"]
            },
            content=f"Completed function {third_response.additional_kwargs['function_call']['name']}",
        ),
    ],
    functions=function_descriptions_multiple,
)

print(fourth_response)
