FROM python:3.13-alpine
COPY ./injection /app
RUN pip install -r /app/requirements.txt
ADD supervisord.conf /usr/local/
WORKDIR /app
ENV FLASK_ENV=development
CMD ["/usr/local/bin/supervisord","-n"]