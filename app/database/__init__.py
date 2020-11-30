#!/usr/bin/env python3
# -*- coding: utf8 -*-
""" module """

from flask import g
import sqlite3

DATABASE = "users_catalog.db"

def get_db():
    db = getattr(g, "_database", None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def output_formatter(results: tuple):
    out = {"body":[]}
    for result in results:
        res_dict = {}
        res_dict["id"] = result[0]
        res_dict["first_name"] = result[1]
        res_dict["last_name"] = result[2]
        res_dict["hobbies"] = result[3]
        out['body'].append(res_dict)
    return out

def scan():
    cursor = get_db().execute("select * from user", ())
    result = cursor.fetchall()
    cursor.close()
    return output_formatter(result)

def read(usr_id):
    query = """
        select *
        from user
        where id = ?
    """
    cursor = get_db().execute(query, (usr_id,))
    result = cursor.fetchall()
    cursor.close()
    return output_formatter(result)

def update(usr_id, fields: dict):
    field_string = ", ".join(
        "%s=\"%s\"" % (key, val)
            for key, val
            in fields.items())
    query = """
            update user
            set %s
            where id = ?
            """ % field_string

    cursor = get_db()
    cursor.execute(query, (usr_id,))
    cursor.commit()
    return True

def create(first_name, last_name, hobbies):
    value_tuple = (first_name, last_name, hobbies)
    query = """
        INSERT INTO user (
            first_name, last_name, hobbies)
        VALUES  (?, ?, ?)
    """
    cursor = get_db()
    last_row_id = cursor.execute(query, value_tuple).lastrowid
    cursor.commit()
    return last_row_id


def delete(usr_id):
    query = "delete from user where id=%s" % usr_id
    cursor = get_db()
    cursor.execute(query, ())
    cursor.commit()
    return True
