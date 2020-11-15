#!/usr/bin/env python3

import json
from json.decoder import JSONDecodeError
import logging
from os import environ

from flask import Flask, request, jsonify
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.exceptions import WebSocketError

from clean import clean
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.DEBUG)

with open('articles.json') as f:
  articles = json.load(f)

model = load_model('articles.h5')
df = pd.read_json('articles_clean.json').astype(str)

def classify(text: str):
  query = clean(text)
  if query == '':
    return None
  logging.debug(f"Normalized request: {query}")

  tokenizer = Tokenizer(num_words=1000)
  tokenizer.fit_on_texts(df['query'].values)

  test = [query]
  xtest = tokenizer.texts_to_matrix(test, mode='binary')
  prediction = model.predict(np.array(xtest))

  id = np.argmax(prediction[0])
  logging.debug(f"Classidied as: {id}")
  return articles[id]

def handle(msg: str):
  try:
    req = json.loads(msg)
    if 'text' in req and isinstance(req['text'], str):
      article = classify(req['text'])
      if article is None:
        return None
      return json.dumps({
        "id": req['id'],
        "text": article['content'],
        "links": [{
          "title": article['title'],
          "link": article['link']
        }],
      })
    return None
  except JSONDecodeError as e:
    logging.error(f"Invalid request: {str(e)}")
    return json.dumps({
      "code": 400,
      "text": str(e)
    })
  except Exception as e:
    logging.error(f"Unkown error: {str(e)}")
    return json.dumps({
      "code": 500,
      "text": str(e)
    })

app = Flask(__name__)
sockets = Sockets(app)

@sockets.route("/api/", methods=["GET"])
def chat(ws):
  while not ws.closed:
    try:
      msg = ws.receive()
      logging.info(f"Processing {msg}")
      res = handle(msg)
      if res is not None:
        ws.send(res)
    except WebSocketError as e:
      logging.error(f"Websocket error: {str(e)}")
    except Exception as e:
      logging.error(f"Error processing request: {str(e)}")

if __name__ == "__main__":
  addr = environ.get('LISTEN_ADDRESS', '0.0.0.0:8080')
  logging.info(f"Listen on {addr}")
  server = pywsgi.WSGIServer(addr, app, handler_class=WebSocketHandler)
  server.serve_forever()
