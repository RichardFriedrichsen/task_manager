FROM python:latest
WORKDIR /app
COPY . /app
CMD python task_manager.py