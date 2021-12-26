# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
import time
import datetime
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

    config.left_quota = int(config.settings["mail_quota"])
    day = datetime.datetime.now().weekday()
    newday = day

    print('start')
    log_writing.ProtSys('Stating main loop and waiting for trigger')
    while True:

        # Setting back the left mail quota on a new day
        newday = datetime.datetime.now().weekday()
        if newday != day:
            config.left_quota = int(config.settings["mail_quota"])
            log_writing.ProtSys('reset Quota to {}'.format(config.left_quota))
        day = newday
        if config.left_quota > 1:
            questioners = imap_interactions.check_inbox()
            if triggers.TimeTrigger() or triggers.ExtTrigger():
                combined_actions.RunAllMails()
                log_writing.ProtSys('set Quota to {}'.format(config.left_quota))
                # After sending out mails waiting for a day (to avoid spam)
                time.sleep(3600*12)
            elif questioners != -1:
                for q in questioners:
                    combined_actions.MailToOne(q)
                    log_writing.ProtSys('set Quota to {}'.format(config.left_quota))
        else:
            # After checking trigers waiting befor doing it agein
            time.sleep(10)


if __name__ == "__main__":
    main()
