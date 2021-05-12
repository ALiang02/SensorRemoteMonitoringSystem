# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: main.py
# @date: 2021/04/24
from routes import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
