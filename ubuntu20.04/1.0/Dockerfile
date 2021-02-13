FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install python3-pip git python3 vim-tiny curl -y && \
    apt-get autoremove -y && \
    apt-get clean

ADD crypto-prometheus/requirements.txt /
RUN pip3 install -r requirements.txt

ENV LOG_LEVEL="WARN" LC_ALL=C.UTF-8 LANG=C.UTF-8

ADD crypto-prometheus/lib /lib
COPY crypto-prometheus/crypto-prometheus.py /crypto-prometheus.py
RUN chown root:root crypto-prometheus.py

EXPOSE 5000

ENTRYPOINT ["/crypto-prometheus.py"]
