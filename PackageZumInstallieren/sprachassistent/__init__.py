import sqlite3
from pathlib import Path
import os, sys

#Setup Brain
filePath = ""
pathParts = os.path.abspath(sys.argv[0]).split("/")
for i in range(len(pathParts) - 1):
    filePath += "/" + pathParts[i]

filePath = filePath[1:]
brainPath = filePath + "/" + "Brain.sqlite"

Brain = Path(brainPath)
if Brain.is_file():                                            #Wenn die Datenbank vorhanden ist, verbindet sich das Programm mit ihr
    connection = sqlite3.connect("Brain.sqlite")
    cursor = connection.cursor()
elif input("Soll eine neue Datenbank angelegt werden(j/n)") == "j": #Wenn eine neue Datenbank angelegt werden soll...
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
else:                                                               #Ausgeben wenn keine Verbindung zu einer Datenbank hergestell wurde, Programm verlassen
    print("Es wurde keine Verbindung zu einer Datenbank hergestellt. Das Programm wird verlassen.")
    exit()
##################
