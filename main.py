#!/usr/bin/env python3

############################################################################################################################
#                                                                                                                          #
#                                                                                                                          #
#   main.py                                                                                                                #
#                                                                                                                          #
#   Copyright 2022 Jacopo Siniscalco <jacopo@siniscalco.eu>                                                                #
#                                                                                                                          #
#   This program is free software; you can redistribute it and/or modify                                                   #
#   it under the terms of the GNU  General Public License as published by                                                  #
#   the Free Software Foundation; either version 3 of the License, or                                                      #
#   (at your option) any later version.                                                                                    #
#                                                                                                                          #
#   This program is distributed in the hope that it will be useful,                                                        #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of                                                         #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                                          #
#   GNU General Public License for more details.                                                                           #
#                                                                                                                          #
#   You should have received a copy of the GNU General Public License                                                      #
#   along with this program; if not, write to the Free Software                                                            #
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,                                                             #
#   MA 02110-1301, USA.                                                                                                    #
############################################################################################################################


import hashlib
from flask import Flask, request

app = Flask (__name__)
app.config['SECRET_KEY'] = "123"

maxqueue = 10
queue = []
messages = {}

@app.route("/post", methods=["post"])
def post():
    data = request.get_data(True, False, False)
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
    for i in range(len(queue)-1,-1,-1):
        output += queue[i] + "\n"
    return output
