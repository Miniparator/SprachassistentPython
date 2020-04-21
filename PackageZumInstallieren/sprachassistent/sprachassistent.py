#-------------------------------------------------------------------------------
# Name:        Sprachassisent
# Purpose:     Ein Sprachassistent fuer Python3.x
#
# Author:      Miniparator
# Version:     0.0.3
# Created:     15.11.2019
#-------------------------------------------------------------------------------

######Bibliotheken importieren######
from tkinter import *
from threading import Thread
from .errors import StateChange #StateChange Fehler imporieren
import speech_recognition as sr
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import sys
import time
import os
import sqlite3
####################################

#Setup Brain
filePath = ""
pathParts = os.path.abspath(sys.argv[0]).split("/")
for i in range(len(pathParts) - 1):
    filePath += "/" + pathParts[i]

filePath = filePath[1:]
brainPath = filePath + "/" + "Brain.sqlite"
                                         #Wenn die Datenbank vorhanden ist, verbindet sich das Programm mit ihr
connection = sqlite3.connect(brainPath)
cursor = connection.cursor()
print("Succesfully connected to Brain.sqlite!")
##################

####Setup Chatterbot####
chatbot = ChatBot('chatbot')                     #Chatbot erstellen
corpusTrainer = ChatterBotCorpusTrainer(chatbot) #Trainer erstellen
corpusTrainer.train("chatterbot.corpus.german")  #Deutsch antrainieren
listTrainer = ListTrainer(chatbot)
########################

####Setup Speech Recognition####
r = sr.Recognizer()
m = sr.Microphone()
print("Bitte kurz leise, Schwelle wird ermittelt...")
with m as source:
    r.adjust_for_ambient_noise(source)
schwelle = r.energy_threshold
################################


class Sprachassistent():
    def __init__(self, name, language, active=False):
        self.Name = name
        self.Language = language
        self.Active = active
        self.__version__ = "0.0.4"
        self.__author__ = "e4rdx"
        self.Schwelle = schwelle

    def infos(self):
        results = {
            "name": self.Name,
            "language": self.Language,
            "schwelle": self.Schwelle,
            "active": self.Active
        }
        return result
        """
        print("Ich heisse", self.Name)
        print("Ich bin", self.Language)
        print("Schwelle ist bei", self.Schwelle)
        if self.Active :
            print("Ich bin aktiv")
        else:
            print("Ich bin nicht aktiv")
        """

    def state(self):
        if self.Active:
            return True
        else:
            return False

    def setActive(self):
        self.Active = True

    def setInactive(self):
        self.Active = False

    def createCommand(self, string) :

        #if string.split(" ")[1] == self.Name :
        #if True:
            if (string.split(" ")[0] == "ok" or string.split(" ")[0] == "okay") and string.split(" ")[1] == self.Name:
                self.Active = True
                return ""

            else:
                erfolg = False

                sql_command = "SELECT * FROM verbenregel;"  #Schleife für suche in verben Tabelle
                cursor.execute(sql_command)
                grundformen = cursor.fetchall()
                words = string.split(" ")
                for x in range(0,len(grundformen)) :
                    form = grundformen[x][2]
                    find = words[0].find(form)
                    if find != -1:
                        if erfolg == False :
                            erfolg = True
                            ergebnis = form
                            type = grundformen[x][3]


                sql_command = "SELECT * FROM andere;"   #Schleife für suche in andere Tabelle
                cursor.execute(sql_command)
                grundformen = cursor.fetchall()
                words = string.split(" ")

                for x in range(0,len(grundformen)) :
                    form = grundformen[x][1]
                    find = words[0].find(form)
                    if find != -1:
                        if erfolg == False :
                            erfolg = True
                            ergebnis = form
                            type = grundformen[x][2]



                if erfolg :             #Wenn etwas passendes gefunden wurde...
                    table = type

                    if type == "verb":
                        table = "verbenregel"
                        form = "grundform"
                    else:
                        form = "name"

                    sql_command = 'SELECT befehl FROM '+table+' WHERE '+form+' = "'+ergebnis+'";'   #SQL um den Befehl zu bekommen
                    cursor.execute(sql_command)
                    arrayCommand = cursor.fetchone()
                    command = arrayCommand[0]


                    if command.find("(") != -1: #Wenn es eine Funktion ist...
                        res = ""
                        for i in range(1,len(words)):
                            res = res + words[i] + " "

                        if res == "":
                            command = command + ")"

                        else:
                            command = command + "'" + res + "'" + ")"

                        return command


                else :
                    raise ValueError


    def answerTo(self,string):
        return chatbot.get_response(string)     #Antwort mit Chatterbot bekommen

    def trainConversation(self, file):
        file = "GespraecheZumTrainieren/" + file                #Angeben das die Datei im Gespraeche Ordner ist
        conversation = open(file, "r")                          #Gegebene Datei Oeffnen
        conversationAsArray = conversation.read().split("\n")   #Datei lesen und in array speichern
        listTrainer.train(conversationAsArray)                  #Mit dem Array den Chatbot trainieren
        conversation.close()                                    #Datei schliessen


    def addCommandVerb(self,grundform,command):
        a = command
        b = grundform
        c = "verb"


        sql_command = 'INSERT INTO verbenregel (ID,befehl,grundform,type) VALUES (NULL,"'+a+'","'+b+'","'+c+'");' #Insert Statement zusammenbauen und ausfuehren
        cursor.execute(sql_command)

        connection.commit()     #Aenderungen speichern

        return True

    def addCommandAndere(self,name,command):
        a = name
        b = command
        c = "andere"

        sql_command = 'INSERT INTO andere (ID,name,befehl,type) VALUES (NULL,"'+a+'","'+b+'","'+c+'");' #Insert Statement zusammenbauen und ausfuehren
        cursor.execute(sql_command)

        connection.commit()     #Aenderungen speichern

        return True

    def say(self,words,speed=120):
        wordsString = str(words)
        speak = 'espeak -v '+ self.Language + ' -s ' + str(speed)+ ' "' + wordsString + '"' #Espeak command erstellen
        os.system(speak)                                                              #Mit OS ausfuehren

    def executeSQL(self, sql_command):
        cursor.execute(sql_command) #SQL ausfuehren
        result = cursor.fetchall()  #Ergebnisse in Array packen

        connection.commit()         #Aenderungen speichern

        return result               #Ergebnis zurueckgeben

    def listen(self):
        global publicWords
        global finishedListener
        global listenerRunning
        publicWords = ""
        listenerRunning = True
        finishedListener = False
        words = ""
        while listenerRunning:
            print("Ready to listen")
            with m as source:
                audio = r.listen(source)
            try:
                words = r.recognize_google(audio, language="de_DE")
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print("No connection to Google Speech Recognition service")
                raise e

            if words != "":
                break
        publicWords = words
        finishedListener = True
        #return words

    def startListener(self):
        thrd = Thread(target=self.listen, args=())
        thrd.start()

    def stopListener():
        global listenerRunning
        listenerRunning = False
        print("Beendigungssignal gesendet")


    def listenerFinished(self):
        global publicWords
        global finishedListener

        if finishedListener:
            return True
        else:
            return False

    def getListener(self):
        global publicWords
        global finishedListener

        if finishedListener:
            return publicWords
        else:
            return None

    def Interface(self, name, width, height):
        connection = sqlite3.connect("Brain.sqlite")
        cursor = connection.cursor()
        window_height = height
        global interfaceOnline

        ####Benoetigte Unterprogramme####
        def execute(event):
            entry_content = entry.get("1.0",'end-1c')
            entry.delete('1.0', END)
            #exec(entry_content)
            command = entry_content.split("/")[0]
            commando = entry_content.split("/")[1]
            if command == "sql":
                cursor.execute(commando) #SQL ausfuehren
                result = cursor.fetchall()  #Ergebnisse in Array packen
                print(result)
                res.delete(1.0, END)
                res.insert(END, result)
        def exit():
            global interfaceOnline
            interfaceOnline = False
        #################################


        ####Fenster erstellen####
        window = Tk()
        window.title('Console ' + name)
        window.geometry(str(height) + "x" + str(width))
        #########################

        ####Elemente erstellen####
        Label(window, text="Enter Command:").place(x=(width/2-50)-50, y=0, width=180, height=30)

        entry = Text(window, width=10)
        entry.bind("<Return>", execute)
        entry.place(x=(width/2-50)-50, y=20, height=200, width=300)

        res = Text(window)
        res.pack()
        res.place(x=(width/2-50)-50, y=240, width=300, height=window_height)

        exitButton = Button(master=window, text='Close', command=exit)
        exitButton.place(x=width-90, y=height-40, width=80, height=30)
        ##########################

        while interfaceOnline:
            window.update()
        window.destroy()    #Fenster schliessen

    def startInterface(self,height,width):
        global interfaceOnline
        interfaceOnline = True
        thrd = Thread(target=self.Interface, args=(self.Name,height,width,))
        thrd.start()

    def stopInterface(self):
        global interfaceOnline
        interfaceOnline = False
