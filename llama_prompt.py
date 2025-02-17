import ollama
from pydantic import BaseModel, Field
import pandas as pd
from typing import Optional
from openai import OpenAI
import json
import base64

# Локалхост оллама
ollama_url = "http://localhost:11434/v1"



class BloodTest(BaseModel):
  indicator: str = Field(..., description="Название показателя анализа крови")
  result: float = Field(..., description="Результат показателя анализа крови")
  measurement: Optional[str] = Field(..., description="Единица измерения показателя анализа крови")

  class Config:
      json_schema_extra = {
          "example": {
              "indicator": "Креатинин",
              "result": 79.0,
              "measurement": "мкмоль/л"
          }
      }

class BloodTestList(BaseModel):
  indicators: list[BloodTest]


def new_llama(url: str, model: str, temp: float, content: str, image_bytes: Optional[bytes] = None):
    # Инициализация клиента для Ollama
    client = OpenAI(base_url=url, api_key="ollama")

    try:
        # Формирование сообщения
        messages = [{"role": "user", "content": content}]

        # Добавление изображения, если оно предоставлено
        if image_bytes:
            # Преобразование байтов в строку для отправки
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            messages.append({"role": "user", "content": f"Изображение: data:image/jpeg;base64,{image_base64}"})

        # Запрос к модели
        response = client.beta.chat.completions.parse(
            model=model,  # Или другая модель, доступная на Ollama
            messages=messages,
            temperature=temp,
            response_format=BloodTestList
        )

        # Извлечение ответа
        json_string = response.choices[0].message.content
        result = json.loads(json_string)
        result = result['indicators']

        # Преобразование в Pandas
        result = pd.DataFrame(result)

        # Заменяем названия столбцов
        if not result.empty:
            new_columns = ["Название", "Значение", "Ед. Измерения"]
            result.columns = new_columns
            result = result.to_json(orient='records', force_ascii=False)
        else:
            return []

        return json.loads(result)

    except Exception as e:
        print(f"Ошибка при работе с Ollama: {e}")

# Запрос к модели Llama 3.2 3B
def llama3b(message, temperature = 0.0):
    response = ollama.generate(
        model="llama3.2:3b",
        prompt=message,  # Передаём сообщение как prompt
        options={
            "temperature": temperature  # Передаём temperature в options
        },
        format=BloodTestList.model_json_schema()
    )
    # Преобразование в json
    json_string = response.response
    result = json.loads(json_string)
    result = result['indicators']

    # Преобразование в Pandas
    result = pd.DataFrame(result)

    # Заменяем названия столбцов
    if not result.empty:
        new_columns = ["Название", "Значение", "Ед. Измерения"]
        result.columns = new_columns

    return result


def llama11b(message, path_image, temperature = 0.0):
    response = ollama.chat(
        model='llama3.2-vision',
        messages=[{
            'role': 'user',
            'content': message,
            'images': [path_image],
            "temperature": temperature
        }],
        format=BloodTestList.model_json_schema()
    )

    # Преобразование в json
    json_string = response.message.content
    result = json.loads(json_string)
    result = result['indicators']

    # Преобразование в Pandas
    result = pd.DataFrame(result)

    # Заменяем названия столбцов
    new_columns = ["Название", "Значение", "Ед. Измерения"]
    result.columns = new_columns

    return result


if __name__ == "__main__":
    text = 'Гемоглобин составляет 3 г/л, хотелось бы побольше, но пока так. Найти в тексте данные анализ крови. Ничего не придумывай'
    res = new_llama(url = ollama_url, model= "llama3.2:3b", temp = 0.0, content = text)
    print(res)
    print(type(res[0]))