#!/usr/bin/env python3
import hashlib
from flask import Flask, request

app = Flask (__name__)
app.config['SECRET_KEY'] = "123"

maxqueue = 10
queue = []
messages = {}

@app.route("/post", methods=["post"])
def post():
    data = request.get_data(False, False, False)
    key = save_data(data)
    print(queue)
    return str(key)

def save_data(inBytes):
    key = hashlib.sha256(inBytes).hexdigest()

    if key in messages:
        return key

    if len(queue) >= maxqueue:
        messages.pop(queue.pop())

    queue.insert(0, key)
    messages[key] = inBytes
    return key

@app.route("/<key>")
def get_post(key):
    if key in messages:
        return messages[key]
    return "no key"

@app.route("/post_id")
def get_id():
    output = ""
    for i in queue:
        output += i + "\n"
    return output
