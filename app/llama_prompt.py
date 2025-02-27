from pydantic import BaseModel, Field
import pandas as pd
from typing import Optional
from openai import OpenAI
import json
import base64
import cv2
# Локалхост оллама
ollama_url = 'http://93.174.229.232:11435/v1'

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


def new_llama(url: str, model: str, temp: float, content: str, image: Optional[str] = None):
    # Инициализация клиента для Ollama
    client = OpenAI(base_url=url, api_key="ollama")

    try:

        # Добавление изображения, если оно предоставлено
        if image:
            # Встраивание изображения как Markdown
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {"type": "text", "text": content},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/png;base64,{image}",
                        },
                    ],
                }
            ]
        else:
            messages = [{"role": "user", "content": content}]

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


if __name__ == "__main__":

    # Проверка без картинки
    text = 'Гемоглобин составляет 3 г/л, хотелось бы побольше, но пока так. Найти в тексте данные анализ крови. Ничего не придумывай'
    res = new_llama(url = ollama_url, model= "llama3.2", temp = 0, content = text)

    # Проверка картинки
    text = 'Найди показатели крови и выведи их'

    # Загрузка картинки
    image_path = 'app/1.jpg'
    image = cv2.imread(image_path)

    # Кодирование изображения в указанный формат
    success, buffer = cv2.imencode('.jpg', image)
    if not success:
        raise ValueError(f"Ошибка при кодировании изображения в формат .jpg")

    # Преобразование в base64
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    res = new_llama(url=ollama_url, model="llama3.2-vision", temp=0, content=text, image = image_base64)

    print(res)