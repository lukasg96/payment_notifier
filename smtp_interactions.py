# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
#_______________________________________________________________________________
import smtplib # sends mails out

import config
import log_writing
#_______________________________________________________________________________
# Sending mail through smtp-server
def testServerLogin():
    '''
    logs onto the server to test login data
    '''
    try:
        server = smtplib.SMTP_SSL(config.settings['smtp_server'], config.settings['smtp_port'])
        #Am Server mit seinen persönlichen Zugangsdaten anmelden
        server.login(config.settings['address'], config.passwd)
        server.ehlo()
        #close connection
        server.quit()
    except smtplib.SMTPAuthenticationError:
        print("Check Password and Server adress.")
        log_writing.ProtSys("Error while logging into SMTP-Server.")
        log_writing.ProtSys("Check Password and Server adress.")
        exit()
    except ConnectionRefusedError:
        log_writing.ProtSys("Connection issue to the SMTP-Server")
        exit()
    except smtplib.SMTPDataError:
        log_writing.ProtSys("Server Problem")
        exit()
    log_writing.ProtSys("Test login successful")
    print("login valid")

def sendMails(mails):
    '''
    Uses all the preconfigured mails and sends them to the SMTP server of the
    mailing provider (t-online in this case).
    
    param mails: list of preconfigured mails
    '''
    try:
        server = smtplib.SMTP_SSL(config.settings['smtp_server'], config.settings['smtp_port'])
        #Am Server mit seinen persönlichen Zugangsdaten anmelden
        server.login(config.settings['address'], config.passwd)
        server.ehlo()
        # Sending of the massages
        for mail in mails:
            try:
                server.send_message(mail)
            except smtplib.SMTPRecipientsRefused:
                log_writing.ProtSys('No mail to' + mail['To'] + '! Check resiver adress!')
            log_writing.ProtMail(mail['To'])
        #close connection
        server.quit()
    
    except smtplib.SMTPAuthenticationError:
        log_writing.ProtSys("Error while logging into SMTP-Server.")
        log_writing.ProtSys("Check Password and Server adress.")
        exit()
    except ConnectionRefusedError:
        log_writing.ProtSys("Connection issue to the SMTP-Server")
    except smtplib.SMTPDataError:
        log_writing.ProtSys("Server Problem")
        log_writing.ProtSys("Massage couldn't be send.")
    finally:
        log_writing.ProtSys("Mails package sent successfully")
