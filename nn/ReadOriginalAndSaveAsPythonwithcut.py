
# import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path

dfdir='../../data/ecalpos/dfdata/'

outdatadir='../../data/nn/tensorflow/'
NbofscanID=3 #5
scanID=[57,58,59,60,61,62,63,64]
startfileID=[164427,172244,175925,183015,191430,195325,202522,210502]
endfileID=[171339,174724,182152,185151,194436,201705,204706,212657]

ledch=39
beamch=47


longimap=[k for k in range(57,65)]
for k in range(49,57):
    longimap.append(k)
for k in reversed(range(1,9)):
    longimap.append(k)
for k in reversed(range(9,17)):
    longimap.append(k)    
longimap=np.array(longimap).reshape(4,8)

def WriteTreeForEachScan():
    scancorr=[0,-0.729162,-0.725412,-0.727109,-0.253724,-0.168832,-0.714801]
    filenamedf=pd.read_csv(dfdir+'filename.csv')
    normvalue=np.loadtxt(dfdir+'normvalueinde.txt')
    filerange=[k for k in range(8,23)]
    Nbofwavepoint=27
    wavearray=np.ones(244).reshape(1,244)
    intarray=np.ones(10).reshape(1,10)
    
    for scanid in range(1,NbofscanID-1):
        for fiid in range(0,33):
            if fiid in filerange:
                if fiid <15:
                    relatedpixels=longimap[:3,scanid-1:scanid+2].reshape(9)
                    relatednorm=normvalue[:3,scanid-1:scanid+2].reshape(9)
                    pos=16-fiid*0.5-10+10
                else:
                    relatedpixels=longimap[1:,scanid-1:scanid+2].reshape(9)
                    relatednorm=normvalue[1:,scanid-1:scanid+2].reshape(9)
                    pos=16-fiid*0.5-6+10
                print(scanid,fiid)
               
                wave,integral=ReadSingleRawText(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixels,relatednorm,Nbofwavepoint)
                # print(np.array(wave).shape,((np.ones(len(integral)).reshape(len(integral),1))*pos).shape)
                # print(np.concatenate((np.array(wave),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=0))
                wavearray=np.concatenate((wavearray,np.concatenate((np.array(wave),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                integral=np.concatenate((intarray,np.concatenate((np.array(integral),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)

        # print(wavearray[1,18:27])
        cnnwave1=wavearray[1:,:9]
        cnnwave2=wavearray[1:,9:18]
        cnnwave3=wavearray[1:,18:27]
        for k in range(1,9):
            cnnwave1=np.concatenate((cnnwave1,wavearray[1:,27*k:27*k+9]),axis=1)
            cnnwave2=np.concatenate((cnnwave2,wavearray[1:,27*k+9:27*k+18]),axis=1)
            cnnwave3=np.concatenate((cnnwave3,wavearray[1:,27*k+18:27*k+27]),axis=1)
        cnnwave=np.concatenate((cnnwave1,cnnwave2,cnnwave3,wavearray[1:,-1].reshape(cnnwave1.shape[0],1)),axis=1)
        # print(cnnwave[0,160:171])
        integral=integral[1:,:]
        wavearray=wavearray[1:,:]
        np.random.shuffle(integral)
        np.random.shuffle(wavearray)
        np.random.shuffle(cnnwave)
        with open(outdatadir+'integralscan'+str(scanid)+'.dat', 'wb') as f:
            pickle.dump(integral, f)
        with open(outdatadir+'wavescan'+str(scanid)+'.dat', 'wb') as f:
            pickle.dump(wavearray, f)
        with open(outdatadir+'cnnwavescan'+str(scanid)+'.dat', 'wb') as f:
            pickle.dump(cnnwave, f)
        print(cnnwave.shape)

def ReadSingleRawText(filename,relatedpixels,relatednorm,Nbofwavepoint):
    firstEvent=True
    wavelist=[]
    intlist=[]
    eventid=-1
    with open(filename,'r') as f:
        for line in f:
            if len(line.split()) > 0:
                line=line.split()
                if line[0]=="Event":
                    eventid+=1
                    if firstEvent:
                        firstEvent=False
                    else:
                        if beamtrigger>4000 and ledtrigger>-500 and ledtrigger<500:
                            # plt.plot(pixelwave[4])
                            # plt.show()
                            wavelist.append(list(pixelwave.reshape(9*Nbofwavepoint)))
                            intlist.append(list(pixelint))
                    pixelwave=np.zeros(9*Nbofwavepoint).reshape(9,Nbofwavepoint)
                    pixelint=np.zeros(9)
                    ledtrigger=0
                    beamtrigger=0
                else:
                    if int(line[0]) in relatedpixels:
                        if len(line[1:])==60:
                            pixelarrayid=np.where(relatedpixels==int(line[0]))[0][0]
                            pixelwave[pixelarrayid,:]=np.array(list(map(int,line[21:21+Nbofwavepoint])))/relatednorm[pixelarrayid]
                            pixelint[pixelarrayid]=sum(list(map(int,line[1:])))/relatednorm[pixelarrayid]
                    elif int(line[0])==ledch:
                        ledtrigger=sum(list(map(int,line[1:])))
                    elif int(line[0])==beamch:
                        beamtrigger=sum(list(map(int,line[1:])))
            if eventid>45000:
                break
        if beamtrigger>4000 and ledtrigger>-500 and ledtrigger<500:
            wavelist.append(list(pixelwave.reshape(9*Nbofwavepoint)))
            intlist.append(list(pixelint))
    return wavelist,intlist

def FindNormValueIndependent():
    filenamedf=pd.read_csv(dfdir+'filename.csv')
    maxpixelvalue=np.zeros(32).reshape(4,8)
    for scanid in range(NbofscanID):
        relatedpixelscolumn=longimap[:,scanid]
        maxpixellist=[]
        for fiid in range(0,33):
            print(scanid,fiid)
            maxpixellist.append(ReadSingleRawTxTforNormIndependent(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixelscolumn))
        maxpixelvalue[:,scanid]=np.array(maxpixellist).min(axis=0)
    np.savetxt(dfdir+'normvalueinde.txt',maxpixelvalue)
    return maxpixelvalue
            

def ReadSingleRawTxTforNormIndependent(filename,relatedpixels):
    eventid=-1
    maxpixelvalue=np.zeros(4)
    with open(filename,'r') as f:
        for line in f:
            if len(line.split()) > 0:
                line=line.split()
                if line[0]=="Event":
                    eventid+=1
                else:
                    if int(line[0]) in relatedpixels:
                        if len(line[1:])>0:
                            pixelarrayid=np.where(relatedpixels==int(line[0]))[0][0]
                            maxpixelvalue[pixelarrayid]=maxpixelvalue[pixelarrayid]+sum(list(map(int,line[1:])))
            # if eventid>1000:
            #     break
        eventid+=1                 
        maxpixelvalue[pixelarrayid]=maxpixelvalue[pixelarrayid]+sum(list(map(int,line[1:])))
    return list(maxpixelvalue/eventid)





WriteTreeForEachScan()







