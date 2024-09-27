FROM docker.io/library/python:3.11.10-alpine3.20

COPY . .
RUN pip install .
RUN cat certs/entrust_g2_ca.cer >> /usr/local/lib/python3.11/site-packages/certifi/cacert.pem
RUN cat certs/entrust_lk1_int.pem >> /usr/local/lib/python3.11/site-packages/certifi/cacert.pem
RUN export REQUESTS_CA_BUNDLE=/usr/local/lib/python3.11/site-packages/certifi/cacert.pem
EXPOSE 5000

CMD ["flask", "--app", "src/run", "run", "--host", "0.0.0.0"]