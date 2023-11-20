#!/usr/bin/env python

"""
Idea: robots.txt + secret link

Routes:
- /
- /robots.txt
- /s3cr3t_3ntry_f0r_r3b3l_b0ts
"""

from flask import Flask, request, render_template
from secret import flag
import random
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/robots.txt', methods=['GET'])
def robots():
    return render_template("robots.txt")

@app.route('/nope', methods=['GET'])
def nope():
    return "Are you Human Spy!?!?!?!"

@app.route('/s3cr3t_3ntry_f0r_r3b3l_b0ts', methods=['GET'])
def secret():
    return (''.join([ random.choice(['0','1']) for i in range(75)]) + flag + ''.join([ random.choice(['0','1']) for i in range(75)]))

app.run(host='0.0.0.0', port=5000, debug=True)