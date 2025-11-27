# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:30:10 2014

@author: fmensing
"""

import maiv2
import csv
import numpy as np
import os

def configADMeasure(cardID, samplerate, channellist = []):
    if channellist == []:
        channellist = range(maiv2.GetADChannels(cardID))
    maiv2.StopMeasure(cardID)
    maiv2.ClearAllChannelLists(cardID)
    for channelID in channellist:
        maiv2.AD_AddChannelToList(cardID, channelID,0,0,1)
    maiv2.AD_SetFrequency(cardID,samplerate)
    maiv2.ConfigMeasure(cardID)

def measureAD2CSV(cardID, filename, numberOfBursts):
    with open(filename, 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ',  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        channelcount = maiv2.AD_GetChannelListSize(cardID)    
        burstsWritten = 0
        maiv2.AD_StartMeasure(cardID)
        while burstsWritten < numberOfBursts:
            valArray = []
            burstsize = maiv2.AD_GetNumberOfValues(cardID)
            if burstsize < 1:
                continue
            for i in range(channelcount):
                column = maiv2.AD_ReadData(cardID,i,burstsize)
                valArray.append(column)
            csvWriter.writerows(np.transpose(valArray))
            burstsWritten += burstsize
            
        maiv2.AD_StopMeasure(cardID)        
    print str(burstsWritten) + " Bursts written to " + os.path.abspath(csvfile.name)