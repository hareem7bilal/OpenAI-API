import requests

url = 'http://127.0.0.1:8000/get_exercise_info'
data = {
    "exercise_name": "push-up"
}

response = requests.post(url, json=data)
print(response.text)