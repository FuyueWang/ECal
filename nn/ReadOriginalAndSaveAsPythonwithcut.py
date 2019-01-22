
# import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path

dfdir='../../data/ecalpos/dfdata/'

outdatadir='../../data/nn/tensorflow/'
NbofscanID=8
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

    for scanid in range(1,5): #NbofscanID-1):
        wavearray1=np.ones(244).reshape(1,244)
        intarray1=np.ones(10).reshape(1,10)
        wavearray2=np.ones(244).reshape(1,244)
        intarray2=np.ones(10).reshape(1,10)
        for fiid in filerange:
            if fiid in filerange:
                if fiid <15:
                    relatedpixels=longimap[:3,scanid-1:scanid+2].reshape(9)
                    relatednorm=normvalue[:3,scanid-1:scanid+2].reshape(9)
                    pos=(fiid-filerange[0])*0.5+1
               
                    wave,integral=ReadSingleRawText(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixels,relatednorm,Nbofwavepoint)
              
                    wavearray1=np.concatenate((wavearray1,np.concatenate((np.array(wave),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                    intarray1=np.concatenate((intarray1,np.concatenate((np.array(integral),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                   
                else:
                    relatedpixels=longimap[1:,scanid-1:scanid+2].reshape(9)
                    relatednorm=normvalue[1:,scanid-1:scanid+2].reshape(9)
                    pos=(fiid-15)*0.5+1
                    wave,integral=ReadSingleRawText(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixels,relatednorm,Nbofwavepoint)
                    wavearray2=np.concatenate((wavearray2,np.concatenate((np.array(wave),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                    intarray2=np.concatenate((intarray2,np.concatenate((np.array(integral),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                print(scanid,fiid)
               
        # print(wavearray1[1,18:27])
        cnnwave1=wavearray1[1:,:9]
        cnnwave2=wavearray1[1:,9:18]
        cnnwave3=wavearray1[1:,18:27]
        for k in range(1,9):
            cnnwave1=np.concatenate((cnnwave1,wavearray1[1:,27*k:27*k+9]),axis=1)
            cnnwave2=np.concatenate((cnnwave2,wavearray1[1:,27*k+9:27*k+18]),axis=1)
            cnnwave3=np.concatenate((cnnwave3,wavearray1[1:,27*k+18:27*k+27]),axis=1)
        cnnwave=np.concatenate((cnnwave1,cnnwave2,cnnwave3,wavearray1[1:,-1].reshape(cnnwave1.shape[0],1)),axis=1)
        # print(cnnwave[0,160:171])
        intarray1=intarray1[1:,:]
        wavearray1=wavearray1[1:,:]
        np.random.shuffle(intarray1)
        np.random.shuffle(wavearray1)
        np.random.shuffle(cnnwave)
        dfint=pd.DataFrame({'label': intarray1[:,-1]})
        dfwave=pd.DataFrame({'label': wavearray1[:,-1]})
        dfcnnwave=pd.DataFrame({'label': cnnwave[:,-1]})
        
        with open(outdatadir+'integralscancenter'+str(scanid)+'row1.dat', 'wb') as f:
            pickle.dump(dict(data=intarray1[:,:-1],label=dfint), f)
        with open(outdatadir+'wavescancenter'+str(scanid)+'row1.dat', 'wb') as f:
            pickle.dump(dict(data=wavearray1[:,:-1],label=dfwave), f)
        with open(outdatadir+'cnnwavescancenter'+str(scanid)+'row1.dat', 'wb') as f:
            pickle.dump(dict(data=cnnwave[:,:-1],label=dfcnnwave), f)
        print(cnnwave.shape)

        # print(wavearray2[1,18:27])
        cnnwave1=wavearray2[1:,:9]
        cnnwave2=wavearray2[1:,9:18]
        cnnwave3=wavearray2[1:,18:27]
        for k in range(1,9):
            cnnwave1=np.concatenate((cnnwave1,wavearray2[1:,27*k:27*k+9]),axis=1)
            cnnwave2=np.concatenate((cnnwave2,wavearray2[1:,27*k+9:27*k+18]),axis=1)
            cnnwave3=np.concatenate((cnnwave3,wavearray2[1:,27*k+18:27*k+27]),axis=1)
        cnnwave=np.concatenate((cnnwave1,cnnwave2,cnnwave3,wavearray2[1:,-1].reshape(cnnwave1.shape[0],1)),axis=1)
        # print(cnnwave[0,160:171])
        intarray2=intarray2[1:,:]
        wavearray2=wavearray2[1:,:]
        np.random.shuffle(intarray2)
        np.random.shuffle(wavearray2)
        np.random.shuffle(cnnwave)
        dfint=pd.DataFrame({'label': intarray2[:,-1]})
        dfwave=pd.DataFrame({'label': wavearray2[:,-1]})
        dfcnnwave=pd.DataFrame({'label': cnnwave[:,-1]})

        with open(outdatadir+'integralscancenter'+str(scanid)+'row2.dat', 'wb') as f:
            pickle.dump(dict(data=intarray2[:,:-1],label=dfint), f)
        with open(outdatadir+'wavescancenter'+str(scanid)+'row2.dat', 'wb') as f:
            pickle.dump(dict(data=wavearray2[:,:-1],label=dfwave), f)
        with open(outdatadir+'cnnwavescancenter'+str(scanid)+'row2.dat', 'wb') as f:
            pickle.dump(dict(data=cnnwave[:,:-1],label=dfcnnwave), f)
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
        if beamtrigger>4000 and ledtrigger>-450 and ledtrigger<450:
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


def WriteDataForEachRow(rowi=1):
    Nbofevents=300000
    wave=np.ones(245).reshape(1,245)
    for scanid in range(1,NbofscanID-1):
        with open(outdatadir+'cnnwavescan'+str(scanid)+'row'+str(rowi)+'.dat', 'rb') as f:
            data=pickle.load(f)
        wave=np.concatenate((wave,np.concatenate((data['data'],data['label'],np.ones(data['label'].shape[0]).reshape(data['label'].shape[0],1)*scanid),axis=1)),axis=0)
    np.random.shuffle(wave)
    dfcnnwave=pd.DataFrame({'label': wave[1:Nbofevents+1,-2],'scan':wave[1:Nbofevents+1,-1]})
    
    with open(outdatadir+'cnnwaverow'+str(rowi)+'.dat', 'wb') as f:
        pickle.dump(dict(data=wave[1:Nbofevents+1,:-2],label=dfcnnwave), f)
    print(wave[1:Nbofevents+1,:-2].shape,dfcnnwave.shape)
WriteTreeForEachScan()







