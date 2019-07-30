#-*- coding: utf-8 -*-

import sqlite3
from bin import config


class Banco(object):

    def __init__(self):
        self.conn = sqlite3.connect(config.databaseFile)
        self.db = self.conn.cursor()

    def execute(self, sql):
        return self.db.execute(sql)

    def executeNonQuery(self, sql):
        self.execute(sql)
        self.conn.commit()
        return self.db.lastrowid

    def executeQuery(self, *sql):
        return self.db.execute(*sql)
