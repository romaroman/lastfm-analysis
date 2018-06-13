FROM alpine:3.5
RUN apk add --update py2-pip
COPY requirements.txt /usr/src/app/
RUN pip install --upgrade setuptools
RUN pip install -r /usr/src/app/requirements.txt
COPY * /usr/src/app/
EXPOSE 4884
