FROM python:3.11-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY calculator/ /app/calculator/
COPY static/ /app/static/
CMD ["uvicorn", "calculator.api:app", "--host", "0.0.0.0", "--port", "80"]