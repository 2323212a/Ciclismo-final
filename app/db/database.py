import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="172.20.217.201",
        user="Admin",
        password="1234",
        database="bicicletas"
    )