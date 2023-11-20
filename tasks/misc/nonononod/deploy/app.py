from flask import Flask, render_template, request
from Levenshtein import distance
import math
import re

app = Flask(__name__)

functions = re.compile(r"get_flag\(.{0,20}\)$|gcd\(.{0,20}\)$", re.I)


def get_flag(magic_word: str = ""):
    if magic_word != "please":
        return "Say magic word as arg. How do you ask your mom?"
    else:
        return "ptctf{l3t_m3_0ut_0f_h3r3}"


def gcd(a, b):
    gcd = math.gcd(a, b)
    return gcd


def sanitize(text: str):
    if not functions.findall(text):
        return f"Wrong function, but levenshtein = {distance(text, 'get_flag()')}"
    else:
        return eval(text)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def form_post():
    try:
        text = request.form['example_text']
        processed_text = sanitize(text)
        return render_template("terminal_answer.html", terminal=processed_text)
    except Exception:
        return render_template("terminal_answer.html", terminal="Unexpected error, try again")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5689, debug=True)
