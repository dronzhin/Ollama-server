from fastapi import FastAPI, UploadFile, File, HTTPException
from llama_prompt import new_llama
from pydantic import BaseModel
import os

app = FastAPI()

# Локалхост оллама
ollama_url = os.getenv('OLLAMA_BASE_URL')
# ollama_url = "http://localhost:11435/v1"

class RequestData(BaseModel):
    model: str
    temp: float
    content: str
    image: UploadFile = File(default=None)  # Делаем поле необязательным

@app.post("/")
async def process_data(data: RequestData):
    image_bytes = None
    if data.image:
        image_bytes = await data.image.read()  # Чтение байтов изображения

    try:
        result = new_llama(
            url=ollama_url,
            model=data.model,
            temp=data.temp,
            content=data.content,
            image_bytes=image_bytes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Обработчик для корневого маршрута (опционально)
@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в API запрос"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)







