ARG PYTHON_IMAGE="python:3.9"
FROM ${PYTHON_IMAGE}

WORKDIR /usr/src/chat

COPY server/requirements.txt .
RUN pip install -r requirements.txt

COPY server .

CMD [ "python3", "server.py" ]
