# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
from email.message import EmailMessage

import config
import validate_address
# ______________________________________________________________________________
# set mail server data


def BuildTable(info):
    '''
    Uses the information of a person to construct a table containing the
    payments the person has to do and the reason why they have to pay that.

    param info: information to a person
    return t: str table with the due pay ments
    '''
    t = '\n| Betrag  | Verwendungszweck'
    t += '\n----------------------------------------------------\n'
    i = 3
    while i < len(info)-1:
        value = str(info[i+1])
        if value == 'nan':
            value = 0
        elif float(value) == 0:
            value = 0
        else:
            t += '| {:6.2f}€ | {}\n'.format(float(value), info[i])
        i += 2
    return t+'\n'


def BildMail(info):
    '''Gets information of a specific person and builds the e-mail for this
    person. This then is put in a EmailMessage() which is defined in the
    package email.message. This contains all necessary propatys of the e-mail.

    param info: list of information to one person
    param ConfigFile: filename where the text that is ont changed is stored
    return message: final configured e-mail
    '''
    receiver = [info[2]]
    receiverName = info[1]  # only first name ist used
    # Seting up mail
    message = EmailMessage()
    message["From"] = config.settings['address']
    message["To"] = receiver

    if info[0] == -1:
        static = open(config.settings['static_mail_err']).read()
        static = static.split('#Cut\n')
        message["Subject"] = static[0]
        content = static[1]

    else:
        # Getting configured Text
        static = open(config.settings['static_mail']).read()
        static = static.split('#Cut\n')
        message["Subject"] = static[0]
        # gets table for mail
        table = BuildTable(info)

        # puts together all parts of the content
        content = static[1] + receiverName + static[2] + table + static[3]
    message.set_content(content)
    return message
