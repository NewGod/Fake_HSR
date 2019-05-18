from fake_hsr import DataBase


def insert_match(form) -> str:
    filed = ["round", "winner id", "loser id", "winner desk id", "loser desk id"]
    for x in filed:
        if x not in form or form[x] == "":
            raise Exception(f"Error: {x} should be filled!")

    with DataBase() as db:
        db.insert("match", form)
    return "success"
# vim: ts=4 sw=4 sts=4 expandtab
