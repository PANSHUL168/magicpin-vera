FROM python:3.14-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# One worker only: conversations and pushed contexts live in this process's memory.
EXPOSE 8080
CMD ["python", "serve.py"]
