FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "imdb_streamlit.py", "runserver", "0.0.0.0:80"]