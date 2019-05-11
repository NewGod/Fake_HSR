from flask import Flask, render_template, request
import os
import click
from database import DataBase
import json


app = Flask(__name__)


@app.cli.command(help="Create the data table.")
@click.option("--file", default="init.sql", type=str, help="the initial sql file.")
@click.option("--database", default="config.json", type=str, help="the sql config file")
def create_table(file, database):
    with DataBase(database) as db:
        db.execute_file(file)


@app.cli.command(help="Insert the cards and desks information.")
@click.option("--dir", default="data/", type=str, help="the data path")
@click.option("--database", default="config.json", type=str, help="the sql config file")
def insert_data(dir_path, database):
    with open(os.path.join(dir_path, "cards.json")) as f:
        for card in json.dump(f):
            with DataBase(database) as db:
                db.add_card(card)
    with open(os.path.join(dir_path, "desks.json")) as f:
        for desk in json.dump(f):
            with DataBase(database) as db:
                db.add_card(desk)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cards", methods=['GET', "POST"])
def card():
    if request.method == "POST":
        print(request.form)
    return render_template('card.html')


# vim: ts=4 sw=4 sts=4 expandtab
