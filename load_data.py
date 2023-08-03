import json
import datetime

from sqlalchemy.sql import text


def insert_into_table(engine, upd_line):
    """ Insert data into table
    """
    x=(
        "INSERT INTO wiki_updates (added_date,total_edit,de_wiki) "
        "VALUES(:added_date, :total_edit, :de_wiki) "
        )   
    query_text = text(x)
    with engine.connect() as conn:
        rs = conn.execute(query_text, {
            "added_date": upd_line['added_date'],
            "total_edit": upd_line['total_edit'],
            "de_wiki": upd_line['de_wiki']})
       