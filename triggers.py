# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
#_______________________________________________________________________________
import datetime

import config
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
    out = bool(float(open(config.settings['external_trigger']).read()))
    if out:
        f = open(config.settings['external_trigger'], 'w')
        f.write('0')
        f.close()
        return True
    else:
        return False
