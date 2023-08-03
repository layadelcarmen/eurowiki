import json
import datetime

from sqlalchemy.sql import text


def create_table(engine):
    """ Create table in postgresql
    """
    query_text = text(
        "CREATE TABLE IF NOT EXISTS wikiupdates (added_date timestamp NOT NULL, total_edit int, de_wiki int );"
        )
    with engine.connect() as conn:
        try:
            rs = conn.execute(query_text)
        except Exception as error:
            print('ERROR: ', error)


def insert_into_table(engine, upd_line):
    """ Insert data into table
    """
    x=(
        "INSERT INTO wikiupdates (added_date,total_edit,de_wiki) "
        "VALUES(:added_date, :total_edit, :de_wiki) "
        )   
    query_text = text(x)
    with engine.connect() as conn:
        rs = conn.execute(query_text, {
            "added_date": upd_line['added_date'],
            "total_edit": upd_line['total_edit'],
            "de_wiki": upd_line['de_wiki']})
       