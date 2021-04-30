FROM python:3.8-alpine

RUN apk update && \
        apk add --no-cache \
        bash

RUN apk add --update build-base python3-dev py-pip

ENV LIBRARY_PATH=/lib:/usr/lib
EXPOSE 5000

WORKDIR /var/usr/comcom
COPY ./*.py /var/usr/comcom/
COPY ./templates/* /var/usr/comcom/templates/

RUN pip install flask
RUN pip install requests

CMD ["python", "main.py"]
