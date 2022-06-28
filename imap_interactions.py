# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
import imaplib

import config
import log_writing
# ______________________________________________________________________________


def check_inbox():
    '''
    This function logs into the imap server of the used mail provider and
    searches the inbox for unseen mails. This way the program replies only
    once to a given mail. From these mails it extracts the address of the
    senders.

    return senders: list of senders of unseen mauls.
    '''
    try:
        # connect to host using SSL
        imap = imaplib.IMAP4_SSL(config.settings['imap_server'])
        # login to server
        imap.login(config.settings['address'], config.passwd)
        # go to inbox
        imap.select('Inbox')
        # grap unseen mails
        tmp, data = imap.search(None, 'UNSEEN')
        if data == [b'']:
            imap.close()
            return -1
    except ConnectionResetError:
        log_writing.ProtSys('did not get Inbox')
        return []
    except:
        log_writing.ProtSys('other error in checking inbox')
        return []
    c = data[0].split()

    # loop over all new mails
    senders = []
    i = 1
    while i <= len(c):
        num = c[-1*i]

        tmp, data = imap.fetch(num, '(RFC822)')
        totmail = data[0][1].decode()
        # extracting address of senders
        st = totmail.find('<')
        sender = totmail[st+1:]
        sender = sender[:sender.find('>')]

        log_writing.ProtSys('Got new mail from'.format(sender))
        senders.append(sender)
        i += 1
    imap.close()
    return senders
