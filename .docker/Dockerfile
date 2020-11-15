ARG PYTHON_IMAGE="python:3.8"
FROM ${PYTHON_IMAGE}

WORKDIR /usr/src/chat

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "server.py" ]
