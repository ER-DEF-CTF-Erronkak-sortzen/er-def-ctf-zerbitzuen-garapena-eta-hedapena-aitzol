FROM python:3-13.0-alpine
RUN pip install -r /app/requirements.txt
COPY ./app /app
WORKDIR /app
ENV FLASK_ENV=development
CMD ["flask", "run"]