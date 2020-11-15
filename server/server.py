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

logging.basicConfig(level=logging.INFO)

with open('articles.json') as f:
  articles = json.load(f)

def classify(text: str):
  return articles[0]

def handle(msg: str):
  try:
    req = json.loads(msg)
    if 'text' in req and isinstance(req['text'], str):
      article = classify(req['text'])
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
