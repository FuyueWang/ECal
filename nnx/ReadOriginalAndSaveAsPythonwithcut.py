
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
   
    filerange=range(0,filenamedf.shape[0]) #range(15,33) #
    for scanid in range(0,1): #Nbofscan):
        wavearray1=np.ones(Nbofwavepoint*9+1).reshape(1,Nbofwavepoint*9+1)
        intarray1=np.ones(10).reshape(1,10)
        wavearray2=np.ones(Nbofwavepoint*9+1).reshape(1,Nbofwavepoint*9+1)
        intarray2=np.ones(10).reshape(1,10)
        wavearray3=np.ones(Nbofwavepoint*9+1).reshape(1,Nbofwavepoint*9+1)
        intarray3=np.ones(10).reshape(1,10)
        for fiid in filerange:
            # print(scanid,fiid)
            if fiid < 15:
                relatedpixels=longimap[scanid:scanid+3,1:4].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,1:4].reshape(9)
                pos=fiid*0.2+10
                wave,integral=ReadSingleRawTxT(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedpixels,relatednorm,Nbofevents,Nbofwavepoint,thisledch=ledch,thisbeamch=beamch)
                
                # print(wavearray.shape,wave.shape,integral.shape[0])
                wavearray1=np.concatenate((wavearray1,np.concatenate((wave,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)
                intarray1=np.concatenate((intarray1,np.concatenate((integral,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)

                
            elif fiid < 33:
                relatedpixels=longimap[scanid:scanid+3,2:5].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,2:5].reshape(9)
                pos=(fiid-15)*0.2+10
                wave,integral=ReadSingleRawTxT(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedpixels,relatednorm,Nbofevents,Nbofwavepoint,thisledch=ledch,thisbeamch=beamch)
                
                # print(wavearray.shape,wave.shape,integral.shape[0])
                wavearray2=np.concatenate((wavearray2,np.concatenate((wave,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)
                intarray2=np.concatenate((intarray2,np.concatenate((integral,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)

            else:
                relatedpixels=longimap[scanid:scanid+3,3:6].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,3:6].reshape(9)
                pos=(fiid-33)*0.2+10
                wave,integral=ReadSingleRawTxT(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedpixels,relatednorm,Nbofevents,Nbofwavepoint,thisledch=ledch,thisbeamch=beamch)
                
                # print(wavearray.shape,wave.shape,integral.shape[0])
                wavearray3=np.concatenate((wavearray3,np.concatenate((wave,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)
                intarray3=np.concatenate((intarray3,np.concatenate((integral,(np.ones(integral.shape[0]).reshape(integral.shape[0],1))*pos),axis=1)),axis=0)

            print(scanid,fiid,pos)
            
        # print(wavearray[1,18:27])
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

        with open(outdatadir+'integralscan'+str(scanid)+'row1.dat', 'wb') as f:
            pickle.dump(dict(data=intarray1[:,:-1],label=dfint), f)
        with open(outdatadir+'wavescan'+str(scanid)+'row1.dat', 'wb') as f:
            pickle.dump(dict(data=wavearray1[:,:-1],label=dfwave), f)
        with open(outdatadir+'cnnwavescan'+str(scanid)+'row1.dat', 'wb') as f:
            pickle.dump(dict(data=cnnwave[:,:-1],label=dfcnnwave), f)
        print(cnnwave.shape)

 # print(wavearray[1,18:27])
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

        with open(outdatadir+'integralscan'+str(scanid)+'row2.dat', 'wb') as f:
            pickle.dump(dict(data=intarray2[:,:-1],label=dfint), f)
        with open(outdatadir+'wavescan'+str(scanid)+'row2.dat', 'wb') as f:
            pickle.dump(dict(data=wavearray2[:,:-1],label=dfwave), f)
        with open(outdatadir+'cnnwavescan'+str(scanid)+'row2.dat', 'wb') as f:
            pickle.dump(dict(data=cnnwave[:,:-1],label=dfcnnwave), f)
        print(cnnwave.shape)


         # print(wavearray3[1,18:27])
        cnnwave1=wavearray3[1:,:9]
        cnnwave2=wavearray3[1:,9:18]
        cnnwave3=wavearray3[1:,18:27]
        for k in range(1,9):
            cnnwave1=np.concatenate((cnnwave1,wavearray3[1:,27*k:27*k+9]),axis=1)
            cnnwave2=np.concatenate((cnnwave2,wavearray3[1:,27*k+9:27*k+18]),axis=1)
            cnnwave3=np.concatenate((cnnwave3,wavearray3[1:,27*k+18:27*k+27]),axis=1)
        cnnwave=np.concatenate((cnnwave1,cnnwave2,cnnwave3,wavearray3[1:,-1].reshape(cnnwave1.shape[0],1)),axis=1)
        
        # print(cnnwave[0,160:171])
        intarray3=intarray3[1:,:]
        wavearray3=wavearray3[1:,:]
        np.random.shuffle(intarray3)
        np.random.shuffle(wavearray3)
        np.random.shuffle(cnnwave)
        dfint=pd.DataFrame({'label': intarray3[:,-1]})
        dfwave=pd.DataFrame({'label': wavearray3[:,-1]})
        dfcnnwave=pd.DataFrame({'label': cnnwave[:,-1]})

        with open(outdatadir+'integralscan'+str(scanid)+'row3.dat', 'wb') as f:
            pickle.dump(dict(data=intarray3[:,:-1],label=dfint), f)
        with open(outdatadir+'wavescan'+str(scanid)+'row3.dat', 'wb') as f:
            pickle.dump(dict(data=wavearray3[:,:-1],label=dfwave), f)
        with open(outdatadir+'cnnwavescan'+str(scanid)+'row3.dat', 'wb') as f:
            pickle.dump(dict(data=cnnwave[:,:-1],label=dfcnnwave), f)
        print(cnnwave.shape)


        
WriteTreeForEachScan()
