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
plotdir="../../plot/dubna/"
rootdatadir="../../data/dubna/rootdata/"

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

def WriteTreeForEachScan():
    Nbofevents=10000
    filenamedf=pd.read_csv(dfdatadir+'energyfilename.csv')
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    filerange=[k for k in range(Nbofenergypos)]
    intch = array('f',9*[0.])
    fileid = array('i',[0])

    for scanid in range(Nbofenergy):
        f = TFile(rootdatadir+"lwaveform"+str(scanid)+"energyless.root", 'recreate' )
        tree = TTree( 'wavetree', 'wavetree' )
        # tree.Branch('wavech',wavech,'wavech[243]/F')
        tree.Branch('intch',intch,'intch[9]/F')
        tree.Branch('fileid',fileid,'fileid/I')
        for fiid in filerange:
            if fiid <7:
                relatedpixels=longienergymap[1:4,3:6].reshape(9)
                relatednorm=normvalue[1:4,3:6].reshape(9)
            else:
                relatedpixels=longienergymap[2:5,3:6].reshape(9)
                relatednorm=normvalue[2:5,3:6].reshape(9)
            print(scanid,fiid)
            fileid[0]=fiid
            intarray=ReadSingleRawTxTReturnIntegral(filenamedf['energy'+str(scanid)].iloc[fiid],relatedpixels,relatednorm,Nbofevents,thisledch=8,thisbeamch=7)
            for itr in range(intarray.shape[0]):
                for k in range(9):
                    intch[k]=intarray[itr,k]
                tree.Fill()
        f.Write()
        f.Close()
# WriteTreeForEachScan()
