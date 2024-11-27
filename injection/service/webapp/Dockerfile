FROM python:3.13-alpine
COPY ./injection /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
ENV FLASK_ENV=development
CMD ["python", "main.py"]