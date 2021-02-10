#!/bin/bash

docker build -t wesparish/crypto-prometheus . && \
  docker push wesparish/crypto-prometheus
