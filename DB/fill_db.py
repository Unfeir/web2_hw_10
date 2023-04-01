import json

import datetime as datetime
from psycopg2 import connect, DatabaseError, Error
from contextlib import contextmanager
from datetime import datetime


@contextmanager
def connection():
    conn = None
    try:
        conn = connect(host='localhost', user='postgres', database='hw_10', password='567234')
        yield conn
    except DatabaseError as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


with open('authors.json', 'r') as fd:
    authors = json.load(fd)

with open('quotes.json', 'r') as fd:
    qoutes = json.load(fd)
    # print(qoutes[0])

##################################################
# authors_insert = []
#
# # print(qoutes[0])
#
# for author in authors:
#     n = author['fullname']
#     d = datetime.strptime(author['date_born'], '%B %d, %Y').date()
#     l = author['location_born']
#     b = author['bio']
#     authors_insert.append(tuple((n, d, l, b)))
#
# print(authors_insert[0])

##################################################
# tags_insert = []
# for qoute in qoutes:
#     tags_insert += qoute['keywords']
#
# tags_insert2 = list(set(tags_insert))
# tags_insert = [(el, tag,) for el, tag in enumerate(tags_insert2, start=1)]
# print(tags_insert)
##################################################

# print(qoutes[:2])




def insert_data(conn, sql, data):
    try:
        c = conn.cursor()
        c.executemany(sql, data)
        c.close()
        conn.commit()
    except DatabaseError as err:
        print(err)


# with connection() as con:
#     sql_to_tag = """INSERT INTO quotes_tag(id, name)
#                            VALUES (%s, %s)"""
#     insert_data(con, sql_to_tag, tags_insert)

# with connection() as con:
#     sql_to_author = """INSERT INTO quotes_author(fullname, born_date, born_location, description)
#                            VALUES (%s, %s, %s, %s)"""
#     insert_data(con, sql_to_author, authors_insert)


##################################################
# with connection() as con:
#     authors_dict = {}
#     quotes_insert = []
#     s_author = """SELECT * from quotes_author"""
#     c = con.cursor()
#     c.execute(s_author)
#     a = c.fetchall()
#
#     for el in a:
#         authors_dict[el[1]] = el[0]
#
#     print(authors_dict)
#
#     for quote in qoutes:
#         author = quote['author']
#         txt = quote['quote']
#         author_id = authors_dict.get(author)
#         quotes_insert.append(tuple((txt, author_id)))
#
#     print(quotes_insert)
#
#     sql_to_quote = """INSERT INTO quotes_note(text, author_id)
#                            VALUES (%s, %s)"""
#     insert_data(con, sql_to_quote, quotes_insert)

##################################################

with connection() as con:
    q_t = []
    qoutes_dict = {}
    tags_dict = {}
    quotes_insert = []
    s_quotes = """SELECT * from quotes_note"""
    s_tags = """SELECT * from quotes_tag"""
    q = con.cursor()
    t = con.cursor()
    q.execute(s_quotes)
    t.execute(s_tags)
    q = q.fetchall()
    t = t.fetchall()

    for el in q:
        qoutes_dict[el[1]] = el[0]

    for el in t:
        tags_dict[el[1]] = el[0]

    print(qoutes_dict)
    print(tags_dict)

    for qoute in qoutes:
        tags = qoute['keywords']
        txt = qoute['quote']
        if tags:
            for tag in tags:
                q_t.append(tuple((qoutes_dict[txt], tags_dict[tag])))

    print(q_t)

    sql_to_q_t = """INSERT INTO quotes_note_tags(note_id, tag_id)
                           VALUES (%s, %s)"""
    insert_data(con, sql_to_q_t, q_t)

