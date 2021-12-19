# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
import getpass
import log_writing
# ______________________________________________________________________________
# Initialization of settings


def InitConfig():
    '''
    Here the needed configurations are read from a config file and the passwort
    is optained from the user (to avoid hard cooding).
    All these configs and the password are stored in global variables.
    '''
    global passwd
    # getpass don't shows what is typed in the terminal other than input()
    passwd = getpass.getpass('E-Mail Password:')

    f = open('config.txt', 'r')
    global settings
    settings = {'address': -1,
                'smtp_server': -1,
                'smtp_port': -1,
                'imap_server': -1,
                'imap_port': -1,
                'mail_quota': -1,
                'spead_sheet_path': -1,
                'sheet': -1,
                'static_mail': -1,
                'static_mail_err': -1,
                'external_trigger': -1,
                'protocol_file': -1
                }
    for line in f:
        if line[0] == '#' or line == '' or line == '\n':
            continue
        line = line.split(': ')
        if line[0] in settings.keys():
            settings[line[0]] = line[1][:-1]
        else:
            print('Warning: stange line found in config.txt')
            print(line)
            continue
    global left_quota
    for c in settings:
        if settings[c] == -1:
            print('config is missing: ', c)
            # When there are not configs missing the program shuts down.
            exit()
    log_writing.ProtSys('Configuration finished')
