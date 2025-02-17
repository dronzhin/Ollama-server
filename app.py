import streamlit as st
import pandas as pd
from PIL import Image
from llama_prompt import new_llama
import io

# Локалхост оллама
ollama_url = "http://localhost:11434/v1"

# Заголовок приложения
st.title("Выбор модели LLaMA")

# Выбор модели
model_choice = st.selectbox("Выберите модель:", ["llama3.2-vision", "llama3.2:3b"])

if model_choice == "llama3.2-vision":
    st.write("Пожалуйста, загрузите изображение и введите промпт.")

    # Загрузка изображения
    uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        # Отображение загруженного изображения
        image = Image.open(uploaded_file)
        st.image(image, caption="Загруженное изображение", use_container_width=True)

    # Ввод промпта
    prompt = st.text_area("Введите промпт:", height=100)  # Промпт на 3 строки

    # Кнопка для вывода результата
    if st.button("Вывести результат"):

        if uploaded_file and prompt:

            # Преобразование изображения в байты
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='JPEG')
            image_bytes = image_bytes.getvalue()

            # Отображение результата
            result = new_llama(url = ollama_url,
                               model= model_choice,
                               temp = 0.0,
                               image_bytes = image_bytes,
                               content = prompt)
            # Преобразуем результат в DataFrame для отображения
            result_df = pd.DataFrame([result])
            st.write("Результаты:")
            st.dataframe(result_df)  # Отображение в виде таблицы
        else:
            st.warning("Пожалуйста, загрузите изображение и введите промпт.")

elif model_choice == "llama3.2:3b":
    st.write("Пожалуйста, введите текст и промпт.")

    # Ввод текста
    text_input = st.text_area("Введите текст:", height=400)  # Текст на 20 строк

    # Ввод промпта
    prompt_input = st.text_area("Введите промпт:", height=100)  # Промпт на 3 строки

    prompt = text_input + ' ' + prompt_input

    # Кнопка для вывода результата
    if st.button("Вывести результат"):
        if text_input and prompt_input:
            # Отображение результата
            result = new_llama(url = ollama_url,
                               model= model_choice,
                               temp = 0.0,
                               content = prompt)
            # Преобразуем результат в DataFrame для отображения
            result_df = pd.DataFrame(result)
            st.write("Результаты:")
            st.dataframe(result_df)  # Отображение в виде таблицы
        else:
            st.warning("Пожалуйста, введите текст и промпт.")





