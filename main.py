# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
#_______________________________________________________________________________
# Import libs
import time

import config
import log_writing
import obtain_data
import configure_massage
import smtp_interactions
import imap_interactions
import triggers
import accessories


def RunAllMails():
    '''
    Runs all necessary functions to build and send mails to all persons with
    pending payments.
    '''
    log_writing.ProtSys('start triggered operation')
    # get data on the people in the spredsheet and removing thos without dept.
    data = obtain_data.DelNonDebtor(obtain_data.ReadTable())
    log_writing.ProtSys('read data from spreadsheet')
    # define vaiable for all mails
    N = len(data)
    mails = [0] * N
    # loop over all depters
    i = 0
    while i < len(data):
        # configured the mail for a person
        mails[i] = configure_massage.BildMail(data[i])
        i += 1
    log_writing.ProtSys('build mails from data')
    #sending all mail to the server
    if N >= int(config.settings['mail_quota']):
        log_writing.ProtSys('mail_quota of {} is larger then Number of Mails {}'\
            .format(config.settings['mail_quota'], N))
        
        N_days = math.ceil(N / int(config.settings['mail_quota']))
        log_writing.ProtSys('The sending of the mails will be done over {} days'\
            .format(math.ceil(N_days)))
        
        #Spliting mail list
        daily_mails = list(accessories.divide_chunks(mails, int(config.settings['mail_quota'])))
        
        for dmails in daily_mails:
            smtp_interactions.sendMails(dmails)
            #the system waits a day
            if dmails != daily_mails[-1]:
                log_writing.ProtSys('Wait for tomorrow')
                time.sleep(3600*24)
    else:
        log_writing.ProtSys('mails can all be send today')
        #ProtSys('sending mail Decoie')
        smtp_interactions.sendMails(mails)
    log_writing.ProtSys('finished triggered operation')

def MailToOne(reciver):
    '''
    Runs all necessary functions to build and send one mail to specified person.
    '''
    data = obtain_data.findDataForAddress(obtain_data.ReadTable(), reciver)
    log_writing.ProtSys('got data of {}'.format(reciver))
    mail = configure_massage.BildMail(data)
    log_writing.ProtSys('build mail from data of {}'.format(reciver))
    smtp_interactions.sendMails([mail])
    log_writing.ProtSys('send mail to {}'.format(reciver))

#_______________________________________________________________________________
# Main function brings all together

def main():
    '''
    Activates the sending if a trigger is set. Than it waits for a day to avoid
    sending out multible mails. If no trigger is set it waits for 100 seconds
    and repeadts the process.
    '''
    config.InitConfig()
    smtp_interactions.testServerLogin()
    log_writing.ProtSys('Stating main loop and waiting for trigger')
    while True:
        questioners = imap_interactions.check_inbox()
        if triggers.TimeTrigger() or triggers.ExtTrigger():
            RunAllMails()
            #After sending out mails waiting for a day (to avoid spam)
            time.sleep(3600*12)
        elif questioners != -1:
            for q in questioners:
                MailToOne(q)
        else:
            # After checking trigers waiting befor doing it agein
            time.sleep(10)


if __name__ == "__main__":
    main()
