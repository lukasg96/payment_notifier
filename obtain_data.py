# Copyright 2021 Lukas Grunwald
# Author: Lukas Grunwald <lukas@grunwald-elzach.de>
# ______________________________________________________________________________
import pandas as pd
import math

import config
# ______________________________________________________________________________
# read finacial data from excel


def ReadTable():
    '''
    Reads all the data from the secified excel spead sheet and puts it in a
    list of one sublist per person (line in speadsheet).

    return data: list variable with all information
    '''
    base_path = config.settings['spead_sheet_path']
    sheet = config.settings['sheet']
    df = pd.read_excel(base_path, sheet)
    data = df.values.tolist()
    return data


def DelNonDebtor(data):
    '''
    Gets a list with all the information and puts people from the list which
    do have to pay something in a new list (so only they get a massage).

    param data: list with people with and wothout dept
    return datanew:
    '''
    datanew = []
    for d in data:
        i = 4
        keep = False
        while i < len(d):
            d[i] = float(d[i])
            # empty cells in spead sheet get translated to nan.
            # Therefor here the program checks also for that.
            if math.isnan(d[i]):
                d[i] = 0.0
            elif d[i] != 0.0:
                keep = True
            i += 2
        if keep:
            datanew.append(d)
    return datanew


def findDataForAddress(data, address):
    for d in data:
        if d[2] == address:
            return d
    return [-1, -1, address]
