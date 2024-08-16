FROM python:3.10-slim
WORKDIR /app/JudgeInfo
RUN pip install flask
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*
CMD ["python", "/app/JudgeInfo/Main.py"]