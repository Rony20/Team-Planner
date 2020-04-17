FROM python:3.7-alpine3.10

WORKDIR /rpbackend

RUN apk add libc-dev make

RUN apk add build-base

COPY . .

# install python requirements
RUN pip install -r ./requirements.txt

# uvicorn runs on port 8000
EXPOSE 8000

# start server
cmd ["python", "start_server.py"]