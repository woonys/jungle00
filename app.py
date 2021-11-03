#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask ,jsonify, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("join.html")


@app.route('/login', methods=['POST'])
def create_card():
    return jsonify({'result': 'fail', 'msg': 'asdasd'})


if __name__ == '__main__':
    app.run()
