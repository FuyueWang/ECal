
import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path
textsize=15
matplotlib.rcParams.update({'font.size': textsize})

txtdatadir="../../data/ecalpos/txtdata/"
dfdatadir="../../data/tradposx/dfdata/"
plotdir="../../plot/nnx/"
outdatadir='../../data/nnx/tensorflow/'
Nbofscan=2

longimap=[k for k in range(57,65)]
longimap+=[k for k in range(49,57)]
longimap+=[k for k in range(25,33)]
longimap+=[k for k in range(17,25)]

longimap=np.array(longimap).reshape(4,8)
ledch=39
beamch=47

          
def ReadSingleRawTxT(filename,relatedtowers,relatedtowersnorm,Nbofevents,Nbofwavepoint,thisledch=ledch,thisbeamch=beamch):
    firstEvent=True
    eventid=-1
    relateddim=relatedtowers.shape[0]
    intlist=[]
    wavelist=[]
    with open(filename,'r') as f:
        for line in f:
            if len(line.split()) > 0:
                line=line.split()
                if line[0]=="Event":
                    eventid+=1
                    if firstEvent:
                        firstEvent=False
                    else:
                        if beamtrigger>0 and ledtrigger<10:
                            # plt.plot(list(pixelwave[4,:]))
                            # plt.show()
                            intlist.append(list(pixelint))
                            wavelist.append(list(pixelwave.reshape(relateddim*Nbofwavepoint)))
                    pixelint=np.zeros(relateddim)
                    pixelwave=np.zeros(relateddim*Nbofwavepoint).reshape(relateddim,Nbofwavepoint)
                    ledtrigger=0
                    beamtrigger=0
                else:
                    if int(line[0]) in relatedtowers:
                        if len(line[1:])==60:
                            pixelarrayid=np.where(relatedtowers==int(line[0]))[0][0]
                            pixelint[pixelarrayid]=sum(list(map(int,line[1:])))/relatedtowersnorm[pixelarrayid]
                            pixelwave[pixelarrayid,:]=np.array(list(map(int,line[20:20+Nbofwavepoint]))) #/relatedtowersnorm[pixelarrayid]
                    elif int(line[0])==thisledch:
                        ledtrigger=sum(list(map(int,line[1:])))
                    elif int(line[0])==thisbeamch:
                        beamtrigger=sum(list(map(int,line[1:])))
            if eventid>Nbofevents:
                break
        if beamtrigger>0 and ledtrigger<10:
            intlist.append(list(pixelint))
            wavelist.append(list(pixelwave.reshape(relateddim*Nbofwavepoint)))
    return np.array(wavelist),np.array(intlist)  #shape: (Nbofevents,relatedtowers.shape[0])

def WriteTreeForEachScan():
    filenamedf=pd.read_csv(dfdatadir+'filename.csv')
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    Nbofwavepoint=27
    Nbofevents=40000
    wavearray=np.ones(Nbofwavepoint*9+1).reshape(1,Nbofwavepoint*9+1)
    intarray=np.ones(10).reshape(1,10)
    filerange=range(15,33) #range(0,filenamedf.shape[0])
    for scanid in range(Nbofscan):
        for fiid in filerange:
            # print(scanid,fiid)
            if fiid < 15:
                relatedpixels=longimap[scanid:scanid+3,1:4].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,1:4].reshape(9)
                pos=fiid*0.2+10
            elif fiid < 33:
                relatedpixels=longimap[scanid:scanid+3,2:5].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,2:5].reshape(9)
                pos=(fiid-15)*0.2+10
            else:
                relatedpixels=longimap[scanid:scanid+3,3:6].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,3:6].reshape(9)
                pos=(fiid-33)*0.2+10
            print(scanid,fiid,pos)
            wave,integral=ReadSingleRawTxT(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedpixels,relatednorm,Nbofevents,Nbofwavepoint,thisledch=ledch,thisbeamch=beamch)
            
            # print(wavearray.shape,wave.shape,integral.shape[0])
            wavearray=np.concatenate((wavearray,np.concatenate((wave,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)
            intarray=np.concatenate((intarray,np.concatenate((integral,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)

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
        intarray=intarray[1:,:]
        wavearray=wavearray[1:,:]
        np.random.shuffle(intarray)
        np.random.shuffle(wavearray)
        np.random.shuffle(cnnwave)
 
        with open(outdatadir+'integralscan'+str(scanid)+'2.dat', 'wb') as f:
            pickle.dump(intarray, f)
        with open(outdatadir+'wavescan'+str(scanid)+'2.dat', 'wb') as f:
            pickle.dump(wavearray, f)
        with open(outdatadir+'cnnwavescan'+str(scanid)+'2.dat', 'wb') as f:
            pickle.dump(cnnwave, f)
        print(cnnwave.shape)
WriteTreeForEachScan()
