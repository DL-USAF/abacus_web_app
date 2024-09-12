FROM docker.io/library/python:3.11.10-alpine3.20

COPY . .
RUN pip install .
EXPOSE 5000

CMD ["flask", "--app", "src/run", "run", "--host", "0.0.0.0"]