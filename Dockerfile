FROM harbor-sh.matrix.co/matrix/crypto_trader:v0.2

WORKDIR /data
COPY . /data

ENTRYPOINT make