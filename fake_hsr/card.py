from typing import Dict, Optional, Sequence
from fake_hsr import DataBase
from pymysql import escape_string, escape_sequence


def cond_constructer(
        column: str,
        value: Sequence,
        nxt: str,
        accept: bool = True
) -> str:
    ret = column
    if not accept:
        ret += " not"
    ret += " in"
    ret += " " + escape_sequence(value, "utf-8") + " " + nxt + " "
    return ret


def card_filter(f: Optional[Dict] = None):
    sql = "select * from `card` a  where "
    if 'name' in f:
        name = f'%{f["name"]}%'
        sql += f"a.`card name` like '{escape_string(name)}' and "
    if 'cost' in f:
        cost = f.getlist('cost')
        if "7" in cost:
            cost.extend([8, 9, 10])
        sql += cond_constructer("a.`cost`", cost, "and")
    if 'class_display' in f:
        if f['class_display'] == 'neutral only':
            sql += cond_constructer("a.`class`", ['Neutral'], "and")
        else:
            sql += cond_constructer("a.`class`", ['Neutral'], "and", False)
    if 'class' in f:
        c = (f['class'], 'Neutral')
        sql += cond_constructer("a.`class`", c, "and")
    if 'rare' in f:
        sql += cond_constructer("a.`rare`", f.getlist('rare'), "and")
    if 'type' in f or 'race' in f or 'mechanism' in f:
        sql += "a.`card id` = Any(select b.`card id` from `card effect state` b join `effect` c on b.`effect id` = c.`effect id` where "
        if 'type' in f:
            sql += cond_constructer("c.`effect type`", f.getlist('type'), "or")
        if 'race' in f:
            sql += cond_constructer("c.`effect type`", f.getlist('race'), "or")
        if 'mechanism' in f:
            sql += cond_constructer("c.`effect type`", f.getlist('mechanism'), "or")
        sql += 'false) and '
    sql += 'true order by a.`cost`'
    with DataBase() as db:
        ret = db.query(sql)
    return ret
