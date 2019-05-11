import os
import json
import MySQLdb
from typing import Dict, Any, Tuple


SqlItem = Dict[str: Any]


def formate_colomn(keys: list) -> str:
    a = '('
    for x in keys:
        assert isinstance(x, str)
        if a[-1] != "(":
            a += f' ,`{x}`'
    a += ')'
    return a


class DataBase:
    address: str
    user: str
    password: str
    config_path: str

    def __init__(self, config_path: str):
        self.config_path = config_path
        with open(self.config_path) as f:
            config = json.load(f)
        self.address = config["address"]
        self.user = config["user"]
        self.password = config["user"]
        self.database = config["database"]
        self._connect()

    def __enter(self):
        return self

    def _connect(self):
        self.db = MySQLdb.connect(
            host=self.address,
            user=self.user,
            passwd=self.password,
            db=self.database
        )
        self.cursor = self.db.cursor()
        self.cursor.execute(f"create database IF NOT EXISTS {self.dababase}")

    def commit(self):
        self.db.commit()

    def exit(self):
        self.commit()
        self.db.close()

    def __exit__(self):
        self.exit()

    def execute(self, cmd: str):
        self.execute(cmd)

    def execute_file(self, path: str):
        with open(path) as f:
            sqlFile = f.read()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            self.cursor.execute(command)

    def insert(self, table: str, item: SqlItem):
        self.cursor.execute(
            f'insert into `{table}` {formate_colomn(item.keys())} \
            value {tuple(item.values())}'
        )
        return self.query("SELECT LAST_INSERT_ID();")[0].values()[0]

    def add_card(self, card: SqlItem):
        effect = card["effect"]
        del card["effect"]
        card_id = self.insert("card", card)
        assert isinstance(effect, dict)
        for x, y in effect.items():
            tmp = self.query('select * form `effect` where `effect type` == {x} \
                       and `description` == {y}')
            if len(tmp) == 0:
                effect_id = self.insert("effect", {"effect type": x, "description": y})
            else:
                effect_id = tmp[0]["effect id"]
            self.insert("card effect state", {"card id": card_id, "effect id": effect_id})

    def add_desk(self, desk: SqlItem):
        cards = desk["cards"]
        del desk["cards"]
        desk_id = self.insert("desk", desk)
        assert isinstance(cards, list)
        for x in cards:
            tmp = self.query('select * form `card` where `card name` == {x} \
                       and `description` == {y}')
            if len(tmp) == 0:
                raise Exception("No this cards: {x}")
            else:
                card_id = tmp[0]["card id"]
            self.insert("card effect state", {"card id": card_id, "desk id": desk_id})

    def add_user(self, user: SqlItem):
        pass

    def add_match(self, match: SqlItem):
        pass

    def query(self, cmd: str, maxrows: int = 0) -> Tuple[SqlItem]:
        self.cursor.query(cmd)
        return self.cursor.fetch_row(maxrows=maxrows, how=1)
