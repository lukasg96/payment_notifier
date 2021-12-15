import config
import log_writing

import imaplib

def check_inbox():
    # connect to host using SSL
    imap = imaplib.IMAP4_SSL(config.settings['imap_server'])
    # login to server
    imap.login(config.settings['address'], config.passwd)
    # go to inbox
    imap.select('Inbox')
    # grap unseen mails
    tmp, data = imap.search(None, 'UNSEEN')
    l = data[0].split()
    if data == [b'']:
        imap.close()
        return -1
    
    # loop over all new mails
    senders = []
    i = 1
    while i <= len(l):
    #for num in l:
        num = l[-1*i]
        
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
