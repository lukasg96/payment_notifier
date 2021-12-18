# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
import time

import config
import validate_address
import log_writing
import obtain_data
import configure_massage
import smtp_interactions
import imap_interactions
import triggers

import combined_actions
# ______________________________________________________________________________
# Main function brings all together


def main():
    '''
    Activates the sending if a trigger is set. Than it waits for a day to avoid
    sending out multible mails. If no trigger is set it waits for 100 seconds
    and repeadts the process.
    '''
    config.InitConfig()
    smtp_interactions.testServerLogin()
    validate_address.checkAll(obtain_data.ReadTable())

    print('start')
    log_writing.ProtSys('Stating main loop and waiting for trigger')
    while True:
        questioners = imap_interactions.check_inbox()
        if triggers.TimeTrigger() or triggers.ExtTrigger():
            combined_actions.RunAllMails()
            # After sending out mails waiting for a day (to avoid spam)
            time.sleep(3600*12)
        elif questioners != -1:
            for q in questioners:
                combined_actions.MailToOne(q)
        else:
            # After checking trigers waiting befor doing it agein
            time.sleep(10)


if __name__ == "__main__":
    main()
