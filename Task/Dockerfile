FROM python:3.8

WORKDIR /Task/Task

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

