# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
from validate_email_address import validate_email

import log_writing
# ______________________________________________________________________________


def check_address(address):
    '''
    Here the validity of a single mail is checked.

    return: boolean stating if mail is valid
    '''
    return validate_email(address, verify=True)


def checkAll(data):
    '''
    This function checks all the addresses contained in a given data set.

    param data: data set extracted from source spreadsheet.
    '''
    allValid = True
    for d in data:
        if check_address(d[2]) is True or check_address(d[2]) is None:
            None
        else:
            allValid = False
            log_writing.ProtSys('The address {} is flase'.format(d[2]))
    if allValid:
        log_writing.ProtSys('All Mails in excel are valid and exist')
        print('all valid')
    log_writing.ProtSys('finnished checking mail addresses')
    print('all mails checked')
