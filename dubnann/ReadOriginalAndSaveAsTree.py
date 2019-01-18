import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path
from decimal import *
import glob
textsize=15
matplotlib.rcParams.update({'font.size': textsize})

txtdatadir="../../data/dubna/txtdata/"
dfdatadir="../../data/dubna/dfdata/"
plotdir="../../plot/dubnann/"
rootdatadir="../../data/dubnann/rootdata/"
outdatadir="../../data/dubnann/tensorflow/"
startfileID=[92816,94900,101529,104121,110138,112425,115316,121433]
endfileID=[94346,100909,103432,105548,111903,113710,120942,122907]

energystartfileID=133634
energyendfileID=151805


Nbofscan=8
Nbofenergy=6
Nbofenergypos=11


longienergymap=[k for k in range(57,65)]
longienergymap+=[k for k in range(49,57)]
longienergymap+=[k for k in reversed(range(33,41))]
longienergymap+=[k for k in reversed(range(41,49))]
longienergymap+=[k for k in range(25,33)]
longienergymap+=[k for k in range(17,25)]

longienergymap=np.array(longienergymap).reshape(6,8)



longimap=[k for k in range(57,65)]
longimap+=[k for k in range(49,57)]
longimap+=[k for k in reversed(range(1,9))]
longimap+=[k for k in reversed(range(9,17))]
longimap+=[k for k in range(25,33)]
longimap+=[k for k in range(17,25)]

longimap=np.array(longimap).reshape(6,8)
ledch=39
beamch=47
# for filepath in glob.iglob(txtdatadir+'076d3e83_20180824_*'):
#     filenamelist.append(filepath)

# # def GetFileName():
# pathlist = Path(txtdatadir).glob('076d3e83_20180824_*')


def GetEnergyFileName():
    filenamedataframe=pd.DataFrame(columns=['energy'+str(k) for k in range(6)])
    filenamelist=[]
    for fileid in range(energystartfileID,energyendfileID+1):
        filename=txtdatadir+'076d3e83_20180826_'+str(fileid)+'.txt'
        if os.path.exists(filename):
            filenamelist.append(filename)

    for k in range(Nbofenergypos-2):
        filenamedataframe.loc[k]=filenamelist[(8-k)*Nbofenergy:(8-k+1)*Nbofenergy]
        print(8-k,8-k+1)


    k=10
    filenamedataframe.loc[9]=filenamelist[k*Nbofenergy:(k+1)*Nbofenergy]
    print(k,k+1)
    k=9
    filenamedataframe.loc[10]=filenamelist[k*Nbofenergy:(k+1)*Nbofenergy]
    print(k,k+1)

    filenamedataframe.to_csv(dfdatadir+'energyfilename.csv')
    return filenamedataframe
# name=GetEnergyFileName()

def GetScanFileName():
    filenamelist=[]
    filenamedataframe=pd.DataFrame()
    for scanid in range(Nbofscan):
        filenamelist=[]
        for fileid in range(startfileID[scanid],endfileID[scanid]+1):
            if fileid<100000:
                filename=txtdatadir+'076d3e83_20180824_0'+str(fileid)+'.txt'
            else:
                filename=txtdatadir+'076d3e83_20180824_'+str(fileid)+'.txt'
            if os.path.exists(filename):
                filenamelist.append(filename)
        if scanid==7:
            filenamelist.append('999')
        filenamedataframe['scanstart'+str(longimap[2,scanid])]=filenamelist
    filenamedataframe.to_csv(dfdatadir+'filename.csv')
    return filenamedataframe
name=GetScanFileName()

def FindNormValueIndependent(plotbefore=False,plotafter=False):
    filenamedf=pd.read_csv(dfdatadir+'filename.csv')
    Nbofevents=20000
    meanintlist_scanid_fiid=[]
    relatedtowersnorm=np.ones(longimap.shape[0])
    normlist=[]
    for scanid in range(Nbofscan):
        meanintlist_scanid=[]
        relatedtowers=longimap[:,scanid].reshape(longimap.shape[0])
        for fiid in range(filenamedf.shape[0]):
            if filenamedf['scanstart'+str(longimap[2,scanid])].iloc[fiid]=='999':
                continue
            print(scanid,fiid)
            intarray=ReadSingleRawTxTReturnIntegral(filenamedf['scanstart'+str(longimap[2,scanid])].iloc[fiid],relatedtowers,relatedtowersnorm,Nbofevents)
            meanintlist_scanid.append(intarray.mean(axis=0))
        meanintlist_scanid_fiid.append(np.array(meanintlist_scanid))
        norm=[np.array(meanintlist_scanid)[:,2].min(), np.array(meanintlist_scanid)[:,3].min()]
        normlist.append(norm)

    normvalue=np.loadtxt('../../data/ecalpos/dfdata/normvalueinde.txt')
    normarray=np.concatenate((normvalue[:2,:],np.array(normlist).T,normvalue[2:,:]),axis=0)
    np.savetxt(dfdatadir+'normvalueinde.txt',normarray)
    
    normedmeanintlist_scanid_fiid=[]
    for scanid in range(Nbofscan):
        normedmeanintlist_scanid_fiid.append(meanintlist_scanid_fiid[scanid]/normarray[:,scanid])
        
    if plotbefore:
        plotmeanintegral(meanintlist_scanid_fiid,plotname='beforenorm')
    if plotafter:
        plotmeanintegral(normedmeanintlist_scanid_fiid,plotname='afternorm')

def plotmeanintegral(meanlist,plotname=''):
    for scanid in range(Nbofscan):
        intarray=meanlist[scanid] #shape: Nboffilesperscan,Nboftowersperscan
        x=[k for k in range(len(meanlist[scanid]))]
        fig = plt.figure(figsize=(7,5))
        ax = plt.subplot2grid((1,1), (0,0))
        for k in range(intarray.shape[1]):
            plt.scatter(x,intarray[:,k], label=str(longimap[k,scanid]))
        plt.legend(loc='upper right')
        plt.xlabel('File ID')
        plt.ylabel('Tower Integral Value')
        if plotname is not '':
            plt.savefig(plotdir+plotname+str(scanid)+'.png',dpi=200)
        plt.show()

        
def ReadSingleRawTxTReturnIntegral(filename,relatedtowers,relatedtowersnorm,Nbofevents,thisledch=ledch,thisbeamch=beamch):
    firstEvent=True
    eventid=-1
    relateddim=relatedtowers.shape[0]
    intlist=[]
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
                            intlist.append(list(pixelint))
                    pixelint=np.zeros(relateddim)
                    ledtrigger=0
                    beamtrigger=0
                else:
                    if int(line[0]) in relatedtowers:
                        if len(line[1:])==60:
                            pixelarrayid=np.where(relatedtowers==int(line[0]))[0][0]
                            pixelint[pixelarrayid]=sum(list(map(int,line[1:])))/relatedtowersnorm[pixelarrayid]
                    elif int(line[0])==thisledch:
                        ledtrigger=sum(list(map(int,line[1:])))
                    elif int(line[0])==thisbeamch:
                        beamtrigger=sum(list(map(int,line[1:])))
            if eventid>Nbofevents:
                break
        if beamtrigger>0 and ledtrigger<10:
            intlist.append(list(pixelint))
    return np.array(intlist)  #shape: (Nbofevents,relatedtowers.shape[0])

# FindNormValueIndependent(plotbefore=True,plotafter=True)


def WriteTreeForEachScan3by4():
    Nbofevents=10000
    filenamedf=pd.read_csv(dfdatadir+'energyfilename.csv')
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    filerange=[k for k in range(Nbofenergypos)]
    intch = array('f',12*[0.])
    fileid = array('i',[0])
    relatedpixels=longienergymap[1:5,3:6].reshape(12)
    relatednorm=normvalue[1:5,3:6].reshape(12)
    for scanid in range(Nbofenergy):
        f = TFile(rootdatadir+"lwaveform"+str(scanid)+"energy3by4.root", 'recreate' )
        tree = TTree( 'wavetree', 'wavetree' )
        # tree.Branch('wavech',wavech,'wavech[243]/F')
        tree.Branch('intch',intch,'intch[12]/F')
        tree.Branch('fileid',fileid,'fileid/I')
        for fiid in filerange:
            print(scanid,fiid)
            fileid[0]=fiid
            intarray=ReadSingleRawTxTReturnIntegral(filenamedf['energy'+str(scanid)].iloc[fiid],relatedpixels,relatednorm,Nbofevents,thisledch=8,thisbeamch=7)
            for itr in range(intarray.shape[0]):
                for k in range(12):
                    intch[k]=intarray[itr,k]
                tree.Fill()
        f.Write()
        f.Close()
        
# from ROOT import TFile, TTree
#WriteTreeForEachScan3by4()
  
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
    Nbofevents=30000
    filenamedf=pd.read_csv(dfdatadir+'energyfilename.csv')
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    filerange=[k for k in range(Nbofenergypos)]
    Nbofwavepoint=27

    for scanid in range(Nbofenergy):
        wavearray1=np.ones(244).reshape(1,244)
        intarray1=np.ones(10).reshape(1,10)
        wavearray2=np.ones(244).reshape(1,244)
        intarray2=np.ones(10).reshape(1,10)
        for fiid in filerange:
            if fiid <5:
                relatedpixels=longienergymap[1:4,3:6].reshape(9)
                relatednorm=normvalue[1:4,3:6].reshape(9)
                pos=(fiid-filerange[0])*0.5+10
                wave,integral=ReadSingleRawTxT(filenamedf['energy'+str(scanid)].iloc[fiid],relatedpixels,relatednorm,Nbofevents,Nbofwavepoint,thisledch=8,thisbeamch=7)
                wavearray1=np.concatenate((wavearray1,np.concatenate((np.array(wave),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                intarray1=np.concatenate((intarray1,np.concatenate((np.array(integral),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
            else:
                relatedpixels=longienergymap[2:5,3:6].reshape(9)
                relatednorm=normvalue[2:5,3:6].reshape(9)
                pos=(fiid-5)*0.5+10
                wave,integral=ReadSingleRawTxT(filenamedf['energy'+str(scanid)].iloc[fiid],relatedpixels,relatednorm,Nbofevents,Nbofwavepoint,thisledch=8,thisbeamch=7)
                wavearray2=np.concatenate((wavearray2,np.concatenate((np.array(wave),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)
                intarray2=np.concatenate((intarray2,np.concatenate((np.array(integral),(np.ones(len(integral)).reshape(len(integral),1))*pos),axis=1)),axis=0)

                
            print(scanid,fiid)

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



WriteTreeForEachScan()
