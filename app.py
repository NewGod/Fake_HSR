from flask import Flask, render_template, request
import os
import click
import json
from fake_hsr import DataBase
from fake_hsr import card_filter


app = Flask(__name__)


@app.cli.command(help="Create the data table.")
@click.option("--file", default="init.sql", type=str, help="the initial sql file.")
@click.option("--database", default="config.json", type=str, help="the sql config file")
def create_table(file, database):
    with DataBase(database) as db:
        db.execute_file(file)


@app.cli.command(help="Insert the cards and desks information.")
@click.option("--dir_path", default="data/", type=str, help="the data path")
@click.option("--database", default="config.json", type=str, help="the sql config file")
def insert_data(dir_path, database):
    with DataBase(database) as db:
        with open(os.path.join(dir_path, "cards.json")) as f:
            for card in json.load(f):
                db.add_card(card)
        with open(os.path.join(dir_path, "desks.json")) as f:
            for desk in json.load(f):
                db.add_desk(desk)
        with open(os.path.join(dir_path, "users.json")) as f:
            for user in json.load(f):
                db.add_user(user)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cards", methods=['GET', "POST"])
def card():
    print(request.form)
    results = card_filter(request.form)
    title = ["cost", "card name", "class", "rare"]
    return render_template('card.html', results=results, titles=title)


# vim: ts=4 sw=4 sts=4 expandtab
