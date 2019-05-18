import os
import json
import pymysql
from typing import Dict, Any, Tuple, Sequence, Optional, Union


SqlItem = Dict[str, Any]
def escape_name(s):
    """Escape name to avoid SQL injection and keyword clashes.

    Doubles embedded backticks, surrounds the whole in backticks.

    Note: not security hardened, caveat emptor.

    """
    return '`{}`'.format(s.replace('`', '``'))



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
        self.commit()
        self.db.close()

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.db.rollback()
        self.db.close()

    def execute(self, cmd: str):
        self.execute(cmd)

    def execute_file(self, path: str):
        with open(path) as f:
            sqlFile = f.read()
        sqlCommands = sqlFile.split(';')
        for x in sqlCommands[:-1]:
            self.cursor.execute(x)

    def insert(self, table: str, item: SqlItem):
        names = list(item.keys())
        cols = ', '.join(map(escape_name, names))  # assumes the keys are *valid column names*.
        placeholders = ', '.join(['%({})s'.format(name) for name in names])

        self.cursor.execute(
            f'insert into `{table}` ({cols}) \
            value ({placeholders})', item
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
        desk["build type"] = desk["name"]
        del desk["name"]
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
        user["player name"] = user["name"]
        cards = user["cards"]
        desks = user["desks"]
        del user["name"]
        del user["cards"]
        del user["desks"]
        player_id = self.insert("player", user)
        for x in cards:
            tmp = self.query('select * from `card` where `card name` = %s;',
                             args=(x,))
            if len(tmp) == 0:
                raise Exception("No this cards: {x}")
            else:
                card_id = tmp[0]["card id"]
            self.insert("player card", {"card id": card_id, "player id": player_id})
        for x in desks:
            tmp = self.query('select * from `desk` where `build type` = %s;',
                             args=(x,))
            if len(tmp) == 0:
                raise Exception("No this desk: {x}")
            else:
                desk_id = tmp[0]["desk id"]
            self.insert("player desk", {"desk id": desk_id, "player id": player_id})

    def add_match(self, match: SqlItem):
        self.insert("match", match)

    def query(self, cmd: str, *, maxrows: int = 0, args: Optional[Union[Sequence, Dict]] = None) -> Tuple[SqlItem]:
        self.cursor.execute(cmd, args)
        if maxrows == 0:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(maxrows)

    def fetch(self):
        return self.cursor.fetch_all()
