# Patchnotes
Beispiele und Beispiel-Funktionen sind 
jetzt <a href="https://github.com/Miniparator/FunktionenFuerSprachassistent/">HIER<a> verfügbar!

# SprachassistentPython
Ein Sprachassistent für Python3.X

# Dependencies
Es wird <a href="chatterbot.readthedocs.io/en/stable/">chatterbot</a> benötigt, damit
der Sprachassistent sich unterhalten kann.
Außerdem wird <a href="pypi.org/project/SpeechRecognition/">speech-recognition</a> benötigt, damit der Sprachinput 
zu einem String verarbeitet werden kann. Und es wird <a href="http://espeak.sourceforge.net/">eSpeak</a>(kann 
unter Linux mit "apt install espeak" installiert werden) zur Sprachausgabe benötigt. Da eSpeak über os 
benutzt wir muss es zu den Pfadvariablen hinzugefügt werden.

# Funktionsweise
In seinem eigenen Programm kann man als Unterprogramme alles was der Assistent können soll
einfügen. Man muss es nur in die Datenbank eintragen(Dazu später mehr). Dann kann man dem Assistenten 
einen String geben, der sofern 
möglich, in einen ausführbaren String umgewandelt wird. Dieser kann dann mit exec() 
ausgeführt werden. Es funtioniert wie folgt:<br>
Das Programm nimmt das erste Wort im Satz und sucht in der Datenbank, ob es einen Befehl dazu gibt.
Wird ein befehl gefunden, setzt das Programm den Rest des Satzes in die Klammern des gefundenen Befehls.<br>
Ein Beispiel:<br>
Eingabe: starte mailservice<br>
In der Datenbank wird der Befehl start() zu dem Wort starte gefunden. Dann wir der Rest, also "mailservice" in die 
Klammern des gefundenen Befehls gesetzt.<br>
Ergebnis: start("mailservice")<br>
Dann kann mit exec() das selbst geschriebene Unterprogramm(z.B.: start(etwas)) aufgerufen werden.<br>


# Benutzung
Wichtig ist, dass sich sprachassistent.py, CreateBrain.py und errors.py in dem gleichen 
Verzeichniswie das Programm befinden. Das sind die drei Dateien die den Sprachassistenten
bilden.<br>
Zuerst muss die Klasse importiert werden:<br>
from sprachassistent import Sprachassistent<br>

Dann kann ein Sprachassistent erstellt werden.
Es wird der Name und die Sprache sowie optional ob er direkt aktiviert ist(default ist False) benötigt.<br>
Beispiel: <br>
example = Sprachassistent("example","german",False)<br>
