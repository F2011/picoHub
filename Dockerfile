# Dockerfile, Image, Container
FROM python:3.12

WORKDIR /picoHub-api

COPY requirements.txt .

# add app-directory
COPY ./app ./app

# add data-directory
COPY ./data ./data

# install dependencies
RUN pip install -r requirements.txt

CMD [ "python", "./app/main.py" ]