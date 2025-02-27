import requests
import os
import cv2
import base64

# 1. Получение списка моделей

# URL для получения списка моделей
ollama_url_models = "http://93.174.229.232:8005/models"
# ollama_url_models = "http://localhost:8005/models"

result = requests.get(ollama_url_models).json()
print(result)

# 2. Использование моделей олама без картинок

ollama_url = "http://93.174.229.232:8005/process"
#ollama_url = "http://localhost:8005/process"

# Переменные для модели
model_choice = 'llama3.2'
temp = 0
prompt = 'Гемоглобин составляет 5 г/л, хотелось бы побольше, но пока так. Найти в тексте данные анализ крови. Ничего не придумывай'

# Подготовка данных для модели
data = {
    "model": model_choice,
    "temp": float(0),
    "content": prompt
}

# Запрос и вывод результата
result = requests.post(ollama_url, data=data).json()
print(result['indicators'])

# 3. Использование моделей олама с картинок

ollama_url = "http://93.174.229.232:8005/process"
# ollama_url = "http://localhost:8005/process"

# Переменные для модели
model_choice = 'llama3.2-vision'
temp = 0
prompt = 'Найти в тексте данные анализ крови. Ничего не придумывай'

# Загрузка картинки
image_path = 'app/1.jpg'
image = cv2.imread(image_path)

# Кодирование изображения в указанный формат
success, buffer = cv2.imencode('.jpg', image)
if not success:
    raise ValueError(f"Ошибка при кодировании изображения в формат .jpg")

# Преобразование в base64
image_base64 = base64.b64encode(buffer).decode('utf-8')

# Проверка существования файла
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Файл {image_path} не найден.")

# Подготовка данных для модели, запрос и вывод результата
with open(image_path, 'rb') as file:
    data = {
        "image": image_base64,
        "model": model_choice,
        "temp": float(temp),
        "content": prompt
    }
    response = requests.post(ollama_url, data=data)

# Обработка ответа
if response.status_code == 200:
    result = response.json()
    print("Результат:", result['indicators'])
else:
    print("Ошибка:", response.status_code, response.text)