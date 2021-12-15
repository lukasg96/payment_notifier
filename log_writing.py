# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
#_______________________________________________________________________________
import datetime
import config
#_______________________________________________________________________________
def stamp():
	'''
	This function saves the current time in a human readabel for into a str.
	To be used in print functions for the state of operations.
	
	return st: string that inclues time
	'''
	st = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+ ' -> '
	return st 

def ProtSys(st):
    '''
    Writes the sytem status in the same file as the mail sending
    
    param st: str to write in protocol
    '''
    f = open(config.settings['protocol_file'], 'a+')
    f.write(stamp() + st + '\n')

#_______________________________________________________________________________
# Write Mail to Protokoll

def ProtMail(reciver):
    '''
    Writs that a may was sent into a file so one can lock it up later.
    Stored is the addres of the reciver and the point in time when the mail
    was send to the person.
    
    param reciver: addres zhe mail was sent to
    '''
    ProtSys('send to {}'.format(reciver))
