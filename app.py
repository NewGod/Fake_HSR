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
    results = card_filter(request.form)
    title = ["cost", "card name", "class", "rare"]
    return render_template('cards.html', results=results, titles=title)


@app.route("/desks", methods=['GET'])
def desk():
    with DataBase() as db:
        desks = db.query("select a.`desk id` `id`, a.`class` `class`, a.`build type` `name`, count(b.`match id`) `match times`, count(if(b.`winner desk id` = a.`desk id`, 1, NULL)) `win`, count(if(b.`loser desk id` = a.`desk id`, 1, NULL)) `lose`, avg(b.`round`) `average round` from `desk` a left join `match` b on a.`desk id` = b.`winner desk id` or a.`desk id` = b.`loser desk id` group by a.`desk id`")
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
        desk = db.query(f"select * from `desk` where `desk id` = {idx}")[0]
        cards = db.query(f"select b.`cost` cost, b.`card name` `card name`, b.`class` `class`, b.`rare` rare from `desk detail` a join `card` b on a.`card id` = b.`card id` where a.`desk id` = {idx} order by b.`cost`, b.`card name`")
    title = ["cost", "card name", "class", "rare"]
    return render_template('desk_detail.html', desk=desk, cards=cards, titles=title)


@app.route("/user")
def user():
    pass


@app.route("/user_detail/<int:idx>")
def user_detail(idx: int):
    pass


@app.match("/match")
def match():
    pass
# vim: ts=4 sw=4 sts=4 expandtab
