# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Hello
   Description :   Flask hello
   Author :        Liangz
   date：          2018/8/4
-------------------------------------------------
   Change Activity:
                   2018/8/4:
-------------------------------------------------
"""
__author__ = 'Liangz'

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)