FROM python:3.13-alpine
COPY ./xss /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0"]