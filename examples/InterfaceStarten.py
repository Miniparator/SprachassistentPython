"""
Startet das Interface des Sprachassistenten und wartet 10 Sekunden.
Dann wird es wieder geschlossen.
"""
from sprachassistent import Sprachassistent
import time

assistent = Sprachassistent("assistent","german")

assistent.startInterface(500,500)#Groesse von Interface mit angeben
time.sleep(10)
assistent.stopInterface()