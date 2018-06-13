FROM alpine:3.5
RUN apk add --update py2-pip
COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
COPY src /usr/src/app/
EXPOSE 4884
