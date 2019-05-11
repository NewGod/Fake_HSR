import os
import json
import pymysql
from typing import Dict, Any, Tuple, Sequence


SqlItem = Dict[str, Any]


def formate_colomn(keys: Sequence[str]) -> str:
    a = '('
    for x in keys:
        if a[-1] != "(":
            a += ' ,'
        a += f"`{x}`"
    a += ')'
    return a


class DataBase:
    address: str
    user: str
    password: str
    config_path: str

    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        with open(self.config_path) as f:
            config = json.load(f)
        self.address = config["address"]
        self.user = config["user"]
        self.password = config["user"]
        self.database = config["database"]
        self._connect()

    def __enter__(self):
        return self

    def _connect(self):
        self.db = pymysql.connect(
            host=self.address,
            user=self.user,
            passwd=self.password,
            db=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.db.cursor()

    def commit(self):
        self.db.commit()

    def exit(self):
        self.db.commit()
        self.db.close()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.exit()
        else:
            self.db.rollback()
            self.db.close()

    def execute(self, cmd: str):
        self.execute(cmd)

    def execute_file(self, path: str):
        with open(path) as f:
            sqlFile = f.read()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands[:-1]:
            self.cursor.execute(command)

    def insert(self, table: str, item: SqlItem):
        self.cursor.execute(
            f'insert into `{table}` {formate_colomn(item.keys())} \
            value {tuple(item.values())}'
        )
        return list(self.query("SELECT LAST_INSERT_ID();")[0].values())[0]

    def add_card(self, card: SqlItem):
        effect = card["effect"]
        del card["effect"]
        card["card name"] = card["name"]
        del card["name"]
        card_id = self.insert("card", card)
        assert isinstance(effect, dict)
        for x, y in effect.items():
            tmp = self.query(f'select * from `effect` where `effect type` = %s and `description` = %s;', args=(x, y))
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
            tmp = self.query('select * from `card` where `card name` = %s;',
                             args=(x,))
            if len(tmp) == 0:
                raise Exception("No this cards: {x}")
            else:
                card_id = tmp[0]["card id"]
            self.insert("desk detail", {"card id": card_id, "desk id": desk_id})

    def add_user(self, user: SqlItem):
        pass

    def add_match(self, match: SqlItem):
        pass

    def query(self, cmd: str, *, maxrows: int = 0, args=None) -> Tuple[SqlItem]:
        self.cursor.execute(cmd, args)
        if maxrows == 0:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(maxrows)

    def fetch(self):
        return self.cursor.fetch_all()
