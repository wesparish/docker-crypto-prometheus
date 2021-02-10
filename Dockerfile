FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install python3-pip git python3 vim-tiny curl -y && \
    pip3 install -r requirements.txt && \
    apt-get autoremove -y && \
    apt-get clean

ENV LOG_LEVEL="WARN" LC_ALL=C.UTF-8 LANG=C.UTF-8

ADD static /static
ADD templates /templates
COPY crypto-prometheus.py /crypto-prometheus.py
RUN chown root:root crypto-prometheus.py

EXPOSE 5000

ENTRYPOINT ["/crypto-prometheus.py"]
CMD ["-s"]
