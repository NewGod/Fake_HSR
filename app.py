from flask import Flask, render_template, request
import os


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


def card_filter(name, hero_class, cose, rare, mechanism, race):
    pass


@app.route("/cards", methods=['GET', "POST"])
def card():
    if request.method == "POST":
        print(request.form)
    return render_template('card.html')


# vim: ts=4 sw=4 sts=4 expandtab
