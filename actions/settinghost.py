import mysql.connector

db_name = "decor_data"

connect = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=db_name
)