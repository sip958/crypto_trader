# I / O

### Input

**Symbol** using a string with `UPPERCASE_UNDERSCORE` format. (e.g. `BTC_USDT`)

**Exchange** using the (class)name of it.

# Services

1. A `Quant Web App` built with `Django`

2. `spiderkeeper`, an open source UI of `scrapyd`

3. `scrapyd`

# Containerize

```bash
# build base image
docker build -t harbor-sh.matrix.co/matrix/crypto_trader_base:0.2 -f ./Dockerfile.base .

# build crypto_trader image
docker build -t harbor-sh.matrix.co/matrix/crypto_trader:1.0 .
```
