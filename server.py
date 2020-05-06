import random

import mysql
from flask import Flask, jsonify, request
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

@server.route("/delete/<urlId>")
def deleteDataById(urlId):
    Id = urlId
    cursor.execute("delete from user where id='"+Id+"'")
    database.commit()
    cursor.execute("select * from user")
    return jsonify(cursor.fetchall())

@server.route("/post",methods=["GET","POST"])
def postData():

    json = request.json
    username = json["username"]
    password = json["password"]
    repeatedPassword = json["repeat"]


    return insertNewRowIntoUserTable(username,password,repeatedPassword,request)


def insertNewRowIntoUserTable(username, password, repeatedPassword, request):

    if(len(username)==0):
        return jsonify("Please enter a username!")

    if (len(password) < 6):

        return jsonify("Please enter a password (at least 6 characters)!")

    if(password != repeatedPassword):

        return jsonify("The passwords are not the same!")

    if(checkIfUsernameExists(username)):

        return jsonify("This username already exists!")

    id = random.randint(0, 10000000)

    while (checkIfIdExists(id)):
        id = random.randint(0, 10000000)

    cursor.execute(
        "insert into user (id,username,password) VALUES ('" + str(id) + "','" + username + "','" + password + "')")
    database.commit()
    return request.json



def checkIfUsernameExists(username):
    usernameColumn = getColumnOfUserTable("username")

    for element in usernameColumn:
        for entry in element:
            if (entry == username):
                return True

    return False

def getColumnOfUserTable(columnName):
    cursor.execute("select " + columnName + " from user")
    result = cursor.fetchall()

    return result


def checkIfIdExists(id):
    idColumn = getColumnOfUserTable("id")

    for element in idColumn:
        for entry in element:
         if(entry==id):
            return True

    return False



if __name__ == "__main__":
    server.run()