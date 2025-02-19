from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from llama_prompt import new_llama  # Импортируйте вашу функцию new_llama

app = FastAPI()

class ResponseModel(BaseModel):
    indicators: list[dict]

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API!"}

@app.post("/process/")
async def process_data(
    model: str,
    temp: float,
    content: str,
    image: UploadFile = File(None)  # Опциональный файл изображения
):
    image_bytes = None
    if image:
        image_bytes = await image.read()  # Чтение байтов изображения

    try:
        result = new_llama(
            url="http://localhost:11434/v1",
            model=model,
            temp=temp,
            content=content,
            image_bytes=image_bytes
        )
        return ResponseModel(indicators=result)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)







