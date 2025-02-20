import requests

ollama_url = "http://localhost:8005"

data = {
    "model": 'llama3.2',
    "temp": 0.0,
    "content": 'Гемоглобин составляет 3 г/л, хотелось бы побольше, но пока так. Найти в тексте данные анализ крови. Ничего не придумывай',
}

result = requests.post(ollama_url, json=data).json()

print(result)