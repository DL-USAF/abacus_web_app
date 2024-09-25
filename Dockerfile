FROM docker.io/library/python:3.11.10-alpine3.20

COPY . .
RUN pip install .
RUN export REQUESTS_CA_BUNDLE=/usr/local/lib/python3.11/site-packages/certifi/cacert.pem
EXPOSE 5000

# CMD ["flask", "--app", "src/run", "run", "--host", "0.0.0.0"]
WORKDIR /src
CMD ["python3", "run.py"]