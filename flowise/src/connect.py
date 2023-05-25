import requests

# Replace with your unqiue URL
API_URL = "http://localhost:3050/api/v1/prediction/6d10d556-c167-4911-8cdf-d22e63a03c3a"


def query(payload):
    response = requests.post(API_URL, json=payload)
    print(response.json())
    return response.json()


output = query(
    {
        "question": "Who is Dave Ebbelaar? And how many subscribers does he have?",
        "memory_key": "chat_history",
        "input_key": "input",
    }
)

output = query(
    {
        "question": "What is that subscriber count multiplied by 4?",
        "memory_key": "chat_history",
        "input_key": "input",
    }
)

output = query(
    {
        "question": "What was my last question?",
        "memory_key": "chat_history",
        "input_key": "input",
    }
)
