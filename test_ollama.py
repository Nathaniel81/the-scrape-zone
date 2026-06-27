import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3",
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly: Hello"
            }
        ],
        "stream": False
    },
    timeout=60
)

print(response.status_code)
print(response.json())