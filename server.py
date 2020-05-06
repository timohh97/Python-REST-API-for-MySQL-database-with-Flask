import random

import mysql
from flask import Flask, jsonify
from mysql import connector

server = Flask(__name__)

database = mysql.connector.connect(host="localhost", user="root", passwd="", database="besucher")

cursor = database.cursor()

@server.route("/")
def startPage():
    return "This is a REST API for a MySQL database"

@server.route("/get")
def getData():
    cursor.execute("select * from user")
    return jsonify(cursor.fetchall())

@server.route("/get/<urlId>")
def getDataById(urlId):
    Id = urlId
    cursor.execute("select * from user where id='"+Id+"'")
    return jsonify(cursor.fetchall())


if __name__ == "__main__":
    server.run()