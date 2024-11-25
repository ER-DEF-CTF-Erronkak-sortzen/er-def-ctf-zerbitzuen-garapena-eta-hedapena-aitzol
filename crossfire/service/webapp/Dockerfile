FROM python:3.13-alpine
COPY ./app /app
RUN pip install -r /app/requirements.txt
WORKDIR /app
ENV FLASK_ENV=development
CMD ["flask", "run"]