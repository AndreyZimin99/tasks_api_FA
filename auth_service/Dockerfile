FROM python:3.11.2

WORKDIR /app

RUN pip install gunicorn==20.1.0 

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .


CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "src.main:auth"]
