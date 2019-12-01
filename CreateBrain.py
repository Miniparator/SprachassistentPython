import sqlite3
connection = sqlite3.connect("Brain.sqlite")

cursor = connection.cursor()


sql_command = """
CREATE TABLE verbenregel (
ID INTEGER PRIMARY KEY,
befehl VARCHAR(30),
grundform VARCHAR(30),
type VARCHAR(30));"""

cursor.execute(sql_command)


sql_command = """
CREATE TABLE andere (
ID INTEGER PRIMARY KEY,
name VARCHAR(30),
type VARCHAR(30),
befehl VARCHAR(30));"""

cursor.execute(sql_command)



#save changes
connection.commit()

connection.close()









