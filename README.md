1. Для формирования контейнера необходимо перейти в папку где находится docker-compose.yml. 
Это основной файл формирования контейнера.
2. В терминале запускаем команду docker compose up -d --build, 
данная команда на основании инструкций docker-compose.yml соберет контейнер.
3. После установки наберите команду docker ps и у вас должно быть запущено два контейнера:
 - ollama-server-api-1
 - ollama-server-ollama-1
4. Установка модели в контейнер ollama-server-ollama-1. Устанавливать необходимо 1 раз в контейнер, после они сохраняются.
Контейнер ollama-server-ollama-1 обязательно должен быть запущен. 
Установка происходит командой docker exec <название контейнера> ollama pull <название модели>:
- docker exec ollama-server-ollama-1 ollama  pull llama3.2 (установка llama3.2:3b)
- docker exec ollama-server-ollama-1 ollama pull llama3.2-vision (установка llama3.2-vision)
- docker exec ollama-server-ollama-1 ollama pull deepseek-r1:14b (установка DeepSeek-R1-Distill-Qwen-14B)
- docker exec ollama-server-ollama-1 ollama run qwen2.5:7b (установка qwen2.5:7b)
- docker exec 9cba3db3ffe3 ollama pull llava:13b (установка llava)
5. После установки будет доступ:
    Списку моделям - http://localhost:8005/models
    К моделям оламы - http://localhost:8005/process
6. Файл example.py примеры получить доступ к серверу