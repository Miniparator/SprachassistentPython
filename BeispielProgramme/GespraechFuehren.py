"""
Beispiel Sprachassistent

Der erstellte Assistent unterhaelt sich mit dem Benutzer
"""

from sprachassistent import Sprachassistent

assistent = Sprachassistent("assistent","german") #Assistent erstellen

#Gespraech antrainieren
assistent.trainConversation("Gespraech1.txt")
assistent.trainConversation("Gespraech2.txt")
assistent.trainConversation("Gespraech3.txt")

print("Press Ctr-C to leave")

while True:
    try:
        assistent.startListener()   #Listener starten

        while not assistent.listenerFinished() :    #Warten bis der listener fertig ist
            pass

        answer = assistent.answerTo(assistent.getListener()) #Antwort zu Gesprochenem in Variable speichern
        print(answer)           #Antwort ausgeben
        assistent.say(answer)   #Antwort sagen
    except KeyboardInterrupt :
        assistent.say("Auf wiedersehen")

