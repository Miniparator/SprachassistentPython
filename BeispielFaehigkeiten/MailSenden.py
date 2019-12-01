import smtplib  

def start(befehl):
    if befehl == "mail":
        
        # Deine Daten muessen hier hin
        senderaddr = ''
        user = ''
        pw = ''
         
        # Gib an, an wen die Mail gesendet werden soll
        receiveraddr  = ''
         
        # Hier kommt die Nachricht hin
        subject = 'BETREFF'
        message = 'Nachricht'
         
        # Mail senden
        mailbody = 'Subject: %s\n\n%s' % (subject, message)
        server = smtplib.SMTP('smtp.googlemail.com:587')
        server.starttls()
        server.login(user,pw)
        server.sendmail(senderaddr, receiveraddr, mailbody)
        server.quit()
