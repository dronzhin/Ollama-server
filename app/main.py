from fastapi import FastAPI, Form, HTTPException
from typing import Optional
from llama_prompt import new_llama
import httpx
import os


app = FastAPI()

# URL для Ollama (лучше использовать переменные окружения)
ollama_url = os.getenv('OLLAMA_BASE_URL', "http://localhost:11435/v1")
ollama_url_models = os.getenv('OLLAMA_MODEL_URL', "http://localhost:11435/api/tags")
# ollama_url='http://93.174.229.232:11435/v1'

@app.post("/process")
async def process_data(
    model: str = Form(...),
    temp: float = Form(...),
    content: str = Form(...),
    image: Optional[str] = Form(None)
):
    try:

        # Вызов функции new_llama
        result = new_llama(
            url=ollama_url,
            model=model,
            temp=temp,
            content=content,
            image=image
        )
        return {"indicators": result}
    except Exception as e:
        print(e)

@app.get("/models")
async def get_models():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(ollama_url_models)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch models")

        data = response.json()
        models = data.get("models", [])
        if not isinstance(models, list):
            raise HTTPException(status_code=500, detail="Invalid response format from Ollama API")
        return [model['name'] for model in models if 'name' in model]
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")

# Обработчик для корневого маршрута (опционально)
@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в API запрос"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)