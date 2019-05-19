from flask import Flask, render_template, request, jsonify
import os
import click
import json
from fake_hsr import DataBase
from fake_hsr import card_filter
from fake_hsr import insert_match


app = Flask(__name__)


@app.cli.command(help="Create the data table.")
@click.option("--file", default="init.sql", type=str, help="the initial sql file.")
@click.option("--database", default=".my.cnf", type=str, help="the sql config file")
def create_table(file, database):
    with DataBase(database) as db:
        db.execute_file(file)


@app.cli.command(help="Insert the cards and desks information.")
@click.option("--dir_path", default="data/", type=str, help="the data path")
@click.option("--database", default=".my.cnf", type=str, help="the sql config file")
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
    results = card_filter(request.form)
    title = ["cost", "card name", "class", "rare"]
    return render_template('cards.html', results=results, titles=title)


@app.route("/desks", methods=['GET'])
def desk():
    with DataBase() as db:
        desks = db.query("select * from `desk view`")
    for x in desks:
        if x["match times"] is None:
            x["winner rate"] = 0
            continue
        tmp = x["win"] + x["lose"] - x["match times"]
        if x["match times"] == tmp:
            x["winner rate"] = 0
        else:
            x["winner rate"] = (x["win"] - tmp) / (x["match times"] - tmp)
    sorted(desks, key=lambda x: x["winner rate"])
    return render_template('desks.html', desks=desks)


@app.route("/desk_detail/<int:idx>")
def desk_detail(idx: int):
    with DataBase() as db:
        desk = db.query("select * from `desk` where `desk id` = %s", args=[int(idx)])[0]
        cards = db.query("select b.`cost` cost, b.`card name` `card name`, b.`class` `class`, b.`rare` rare from `desk detail` a join `card` b on a.`card id` = b.`card id` where a.`desk id` = %s order by b.`cost`, b.`card name`", args=[int(idx)])
    title = ["cost", "card name", "class", "rare"]
    return render_template('desk_detail.html', desk=desk, cards=cards, titles=title)


@app.route("/match", methods=['GET', "POST"])
def match():
    info = None
    if request.method == "POST":
        try:
            insert_match(request.form)
            info = "Success!"
        except Exception as e:
            info = str(e)
    with DataBase() as db:
        players = db.query("select * from `player` order by `player id`")
    return render_template('match.html', players=players, info=info)


@app.route("/get_player_desk/<int:idx>")
def get_player_desk(idx: int):
    with DataBase() as db:
        desks = db.query('select `desk id` id, `name` name from `player desk view` where `player id`=%s order by `desk id`', args=[int(idx)])
    return jsonify(desks)


@app.route("/report")
def report():
    return render_template('report.html')
# vim: ts=4 sw=4 sts=4 expandtab
