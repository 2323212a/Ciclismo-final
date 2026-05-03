import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="bike_user",
        password="1234",
        database="bicicletas"
    )