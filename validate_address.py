# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
#_______________________________________________________________________________

# validate-email-address
# py3dns
from validate_email_address import validate_email

import log_writing
#_______________________________________________________________________________
def check_address(address):
    return validate_email(address, verify=True)
#_______________________________________________________________________________
def checkAll(data):
    allValid = True
    for d in data:
        if check_address(d[2]) == True or check_address(d[2]) == None:
            None
        else:
            allValid = False
            log_writing.ProtSys('The address {} is flase'.format(d[2]))
    if allValid:
        log_writing.ProtSys('All Mails in excel are valid and exist')
        print('all valid')
    log_writing.ProtSys('finnished checking mail addresses')
    print('all mails checked')
