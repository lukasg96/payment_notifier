# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
#_______________________________________________________________________________
# Import libs
import pandas as pd
import smtplib # sends mails out
from email.message import EmailMessage
import time
import datetime
import numpy as np
import math
import getpass
#_______________________________________________________________________________
def stamp():
	'''
	This function saves the current time in a human readabel for into a str.
	To be used in print functions for the state of operations.
	
	return st: string that inclues time
	'''
	st = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ ' -> '
	return st 

def ProtSys(st):
    '''
    Writes the sytem status in the same file as the mail sending
    
    param st: str to write in protocol
    '''
    f = open(configs['protocol_file'], 'a+')
    f.write(stamp() + st + '\n')
#_______________________________________________________________________________
# Initialization of settings
def InitConfig():
    '''
    Here the needed configurations are read from a config file and the passwort
    is optained from the user (to avoid hard cooding). All these configs and the
    password are stored in global variables.
    '''
    global passwd
    # getpass don't shows what is typed in the terminal other than input()
    passwd = getpass.getpass('E-Mail Password:')
    
    #print(stamp() + 'Reading Config')
    f = open('config.txt', 'r')
    global configs
    configs = {'address': -1,
                'smtp_server': -1,
                'port' : -1,
                'mail_quota' : -1,
                'spead_sheet_path' : -1,
                'sheet' : -1,
                'static_mail' : -1,
                'external_trigger' : -1,
                'protocol_file' : -1
                }
    for l in f:
        if l[0] == '#' or l == '' or l == '\n':
            continue
        l = l.split(': ')
        if l[0] in configs.keys():
            configs[l[0]] = l[1][:-1]
            #print(configs[l[0]])
        else:
            print('Warning: stange line found in config.txt')
            print(l)
            continue
    for c in configs:
        if configs[c] == -1:
            print ('config is missing: ', c)
            # When there are not configs missing the program shuts down.
            exit()
    ProtSys('Configuration finished')

#_______________________________________________________________________________
# read finacial data from excel
def ReadTable():
    '''
    Reads all the data from the secified excel spead sheet and puts it in a list
    of one sublist per person (line in speadsheet).
    
    return data: list variable with all information
    '''
    base_path = configs['spead_sheet_path']
    sheet = configs['sheet']
    df = pd.read_excel(base_path , sheet)
    data = df.values.tolist()
    return data

def DelNonDebtor(data):
    '''
    Gets a list with all the information and puts people from the list which
    do have to pay something in a new list (so only they get a massage).
    
    param data: list with people with and wothout dept
    return datanew:
    '''
    datanew = []
    for d in data:
        i = 4
        keep = False
        while i < len(d):
            d[i] = float(d[i])
            # empty cells in spead sheet get translated to nan.
            # Therefor here the program checks also for that.
            if math.isnan(d[i]):
                d[i] = 0.0
            if d[i] != 0.0:
                keep = True
            i += 2
        if keep:
            datanew.append(d)
    return datanew
    
#_______________________________________________________________________________
# set mail server data 
def BuildTable(info):
    '''
    Uses the information of a person to construct a table containing the
    payments the person has to do and the reason why they have to pay that.
    
    param info: information to a person
    return t: str table with the due pay ments
    '''
    t = '\n|  Betrag  | Verwendungszweck'
    t+= '\n----------------------------------------------------\n'
    i = 3
    while i < len(info)-1:
        value = str(info[i+1])
        if value == 'nan':
            value = 0
        elif float(value) == 0:
            value = 0
        else:
            #print(value, info[i])
            t += '| {:6.2f}€ | {}\n'.format(float(value), info[i])#
        i += 2
    #print(t)
    return t+'\n'
    
def BildMail(info, ConfigFile):
    '''Gets information of a specific person and builds the e-mail for this
    person. This then is put in a EmailMessage() which is defined in the package
    email.message. This contains all necessary propatys of the e-mail.
    
    param info: list of information to one person
    param ConfigFile: filename where the text that is ont changed is stored
    return message: final configured e-mail
    '''
    receiver = [info[2]]
    receiverName = info[1]
    
    # Getting configured Text
    static = open(ConfigFile).read()
    static = static.split('#Cut\n')
    
    # Seting up mail
    message = EmailMessage()
    message["Subject"] = static[0]
    message["From"] = configs['address']
    message["To"] = receiver
    
    # gets table for mail
    table = BuildTable(info)
    
    # puts together all parts of the content
    content = static[1] + receiverName + static[2] + table + static[3]
    message.set_content(content)
    return message
#_______________________________________________________________________________
# Write Mail to Protokoll

def ProtMail(reciver):
    '''
    Writs that a may was sent into a file so one can lock it up later.
    Stored is the addres of the reciver and the point in time when the mail
    was send to the person.
    
    param reciver: addres zhe mail was sent to
    '''
    ProtSys('send to {}'.format(reciver))

#_______________________________________________________________________________
# Sending mail through smtp-server
def testServerLogin():
    '''
    logs onto the server to test login data
    '''
    try:
        server = smtplib.SMTP_SSL(configs['smtp_server'], configs['port'])
        #Am Server mit seinen persönlichen Zugangsdaten anmelden
        server.login(configs['address'], passwd)
        server.ehlo()
        #close connection
        server.quit()
    except smtplib.SMTPAuthenticationError:
        print("Check Password and Server adress.")
        ProtSys("Error while logging into SMTP-Server.")
        ProtSys("Check Password and Server adress.")
        exit()
    except ConnectionRefusedError:
        ProtSys("Connection issue to the SMTP-Server")
    except smtplib.SMTPDataError:
        ProtSys("Server Problem")
        ProtSys("Massage couldn't be send.")
    ProtSys("Test login successful")
    print("login valid")

def sendMails(mails):
    '''
    Uses all the preconfigured mails and sends them to the SMTP server of the
    mailing provider (t-online in this case).
    
    param mails: list of preconfigured mails
    '''
    try:
        server = smtplib.SMTP_SSL(configs['smtp_server'], configs['port'])
        #Am Server mit seinen persönlichen Zugangsdaten anmelden
        server.login(configs['address'], passwd)
        server.ehlo()
        # Sending of the massages
        for mail in mails:
            server.send_message(mail)
            ProtMail(mail['To'])
        #close connection
        server.quit()
    
    except smtplib.SMTPAuthenticationError:
        ProtSys("Error while logging into SMTP-Server.")
        ProtSys("Check Password and Server adress.")
        exit()
    except ConnectionRefusedError:
        ProtSys("Connection issue to the SMTP-Server")
    except smtplib.SMTPDataError:
        ProtSys("Server Problem")
        ProtSys("Massage couldn't be send.")
    finally:
        ProtSys("Mails package sent successfully")

#_______________________________________________________________________________
# Do all of the mail
def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]


def RunAllMails():
    '''
    Runs all necessary functions to build and send mails to all persons with
    pending payments.
    '''
    ProtSys('start triggered operation')
    # get data on the people in the spredsheet and removing thos without dept.
    data = DelNonDebtor(ReadTable())
    ProtSys('read data from spreadsheet')
    # define vaiable for all mails
    N = len(data)
    mails = [0] * N
    # loop over all depters
    i = 0
    while i < len(data):
        # configured the mail for a person
        mails[i] = BildMail(data[i], configs['static_mail'])
        i += 1
    ProtSys('build mails from data')
    #sending all mail to the server
    if N >= int(configs['mail_quota']):
        ProtSys('mail_quota of {} is larger then Number of Mails {}'\
            .format(configs['mail_quota'], N))
        
        N_days = math.ceil(N / int(configs['mail_quota']))
        ProtSys('The sending of the mails will be done over {} days'\
            .format(math.ceil(N_days)))
        
        #Spliting mail list
        daily_mails = list(divide_chunks(mails, int(configs['mail_quota'])))
        
        for dmails in daily_mails:
            sendMails(dmails)
            #the system waits a day
            if dmails != daily_mails[-1]:
                ProtSys('Wait for tomorrow')
                time.sleep(3600*24)
    else:
        ProtSys('mails can all be send today')
        #ProtSys('sending mail Decoie')
        sendMails(mails)
    ProtSys('finished triggered operation')

#_______________________________________________________________________________
# Triggering the sending

def TimeTrigger():
    '''
    Checks if it is the time to send the mails to everyboty with dept.
    In this case I chosen satturday at noon for this.
    
    return: bool vaiable that is ony true if the time is come.
    '''
    now = datetime.datetime.today()
    # for every other satturday add: now.isocalendar()[1]%2 == 0
    if now.weekday() == 5 and now.hour == 12:
        return True
    else:
        return False

def ExtTrigger():
    '''
    Checks if a external trigger in a specified file is active. If that is the
    case it is set back to 0 and a True is returnd.
    
    return: bool vaiable that is ony true if external trigger was set.
    '''
    out = bool(float(open(configs['external_trigger']).read()))
    if out:
        f = open(configs['external_trigger'], 'w')
        f.write('0')
        f.close()
        return True
    else:
        return False

#_______________________________________________________________________________
# Main function brings all together

def main():
    '''
    Activates the sending if a trigger is set. Than it waits for a day to avoid
    sending out multible mails. If no trigger is set it waits for 100 seconds
    and repeadts the process.
    '''
    InitConfig()
    testServerLogin()
    ProtSys('Stating main loop and waiting for trigger')
    while True:
        if TimeTrigger() or ExtTrigger():
            RunAllMails()
            #After sending out mails waiting for a day (to avoid spam)
            time.sleep(3600*24)
        else:
            # After checking trigers waiting befor doing it agein
            time.sleep(100)

if __name__ == "__main__":
    main()
