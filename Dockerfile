FROM harbor-sh.matrix.co/matrix/crypto_trader_base:0.1

WORKDIR /data
ADD . /data

EXPOSE 6800

CMD /bin/bash
