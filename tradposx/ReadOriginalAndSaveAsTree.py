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

txtdatadir="../../data/ecalpos/txtdata/"
dfdatadir="../../data/tradposx/dfdata/"
plotdir="../../plot/tradposx/"
rootdatadir="../../data/tradposx/rootdata/"

startfileIDy=[92816,94900,101529,104121,110138,112425,115316,121433]
endfileIDy=[94346,100909,103432,105548,111903,113710,120942,122907]
startfileIDx=[172330,140653]
endfileIDx=[155051,152923]
energystartfileID=133634
energyendfileID=151805


Nbofscan=2

longimap=[k for k in range(57,65)]
longimap+=[k for k in range(49,57)]
longimap+=[k for k in range(25,33)]
longimap+=[k for k in range(17,25)]

longimap=np.array(longimap).reshape(4,8)
ledch=39
beamch=47
# for filepath in glob.iglob(txtdatadir+'076d3e83_20180824_*'):
#     filenamelist.append(filepath)

# # def GetFileName():
# pathlist = Path(txtdatadir).glob('076d3e83_20180824_*')

def GetScanFileName(startfileID=startfileIDx,endfileID=endfileIDx,date='25',starttower=[51,27]):
    filenamelist=[]
    filenamedataframe=pd.DataFrame()
    for scanid in range(Nbofscan):
        filenamelist=[]
        if startfileID[scanid]<endfileID[scanid]:
            fileidrange=range(startfileID[scanid],endfileID[scanid]+1)
        else:
            fileidrange=reversed(range(endfileID[scanid],startfileID[scanid]+1))
        for fileid in fileidrange:
            filename=txtdatadir+'076d3e83_201808'+date+'_'+str(fileid)+'.txt'
            if os.path.exists(filename):
                filenamelist.append(filename)
        filenamedataframe['scanstart'+str(starttower[scanid])]=filenamelist
    filenamedataframe.to_csv(dfdatadir+'filename.csv')
    return filenamedataframe
# name=GetScanFileName()

                          
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


def plotmeanintegral(meanlist,plotname=''):
    for scanid in range(Nbofscan):
        intarray=meanlist[scanid] #shape: Nboffilesperscan,Nboftowersperscan
        x=[k for k in range(len(meanlist[scanid]))]
        fig = plt.figure(figsize=(7,5))
        ax = plt.subplot2grid((1,1), (0,0))
        for k in range(intarray.shape[1]):
            plt.scatter(x,intarray[:,k], label=str(longimap[scanid+1,k+2]))
        plt.legend(loc='upper right')
        plt.xlabel('File ID')
        plt.ylabel('Tower Integral Value')
        if plotname is not '':
            plt.savefig(plotdir+plotname+str(scanid)+'.png',dpi=200)
        plt.show()
        

def checknorm():
    filenamedf=pd.read_csv(dfdatadir+'filename.csv')
    Nbofevents=2000
    meanintlist_scanid_fiid=[]
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    for scanid in range(Nbofscan):
        meanintlist_scanid=[]
        relatedtowers=longimap[scanid+1,2:6].reshape(4)
        relatedtowersnorm=normvalue[scanid+1,2:6].reshape(4)
        for fiid in range(filenamedf.shape[0]):
            print(scanid,fiid)
            intarray=ReadSingleRawTxTReturnIntegral(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedtowers,relatedtowersnorm,Nbofevents)
            meanintlist_scanid.append(intarray.mean(axis=0))
        meanintlist_scanid_fiid.append(np.array(meanintlist_scanid))
    plotmeanintegral(meanintlist_scanid_fiid,plotname='afternorm')

# checknorm()

def WriteTreeForEachScan3by6():
    Nbofevents=1000
    filenamedf=pd.read_csv(dfdatadir+'filename.csv')
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    intch = array('f',18*[0.])
    fileid = array('i',[0])
    for scanid in range(Nbofscan):
        relatedpixels=longimap[scanid:scanid+3,1:7].reshape(18)
        relatednorm=normvalue[scanid:scanid+3,1:7].reshape(18)
        
        f = TFile(rootdatadir+"lwaveform"+str(scanid)+"energy3by6.root", 'recreate' )
        tree = TTree( 'wavetree', 'wavetree' )
        # tree.Branch('wavech',wavech,'wavech[243]/F')
        tree.Branch('intch',intch,'intch[18]/F')
        tree.Branch('fileid',fileid,'fileid/I')
        for fiid in range(filenamedf.shape[0]):
            print(scanid,fiid)
            fileid[0]=fiid
            intarray=ReadSingleRawTxTReturnIntegral(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedpixels,relatednorm,Nbofevents,thisledch=ledch,thisbeamch=beamch)
            for itr in range(intarray.shape[0]):
                for k in range(18):
                    intch[k]=intarray[itr,k]
                tree.Fill()
        f.Write()
        f.Close()
        
from ROOT import TFile, TTree
# WriteTreeForEachScan3by6()

def WriteTreeForEachScan():
    Nbofevents=30000
    filenamedf=pd.read_csv(dfdatadir+'filename.csv')
    normvalue=np.loadtxt(dfdatadir+'normvalueinde.txt')
    intch = array('f',9*[0.])
    fileid = array('i',[0])

    for scanid in range(Nbofscan):
        f = TFile(rootdatadir+"lwaveform"+str(scanid)+"energy.root", 'recreate' )
        tree1 = TTree( 'wavetreerow1', 'wavetree' )
        # tree1.Branch('wavech',wavech,'wavech[243]/F')
        tree1.Branch('intch',intch,'intch[9]/F')
        tree1.Branch('fileid',fileid,'fileid/I')
        tree2 = TTree( 'wavetreerow2', 'wavetree' )
        # tree2.Branch('wavech',wavech,'wavech[243]/F')
        tree2.Branch('intch',intch,'intch[9]/F')
        tree2.Branch('fileid',fileid,'fileid/I')
        tree3 = TTree( 'wavetreerow3', 'wavetree' )
        # tree3.Branch('wavech',wavech,'wavech[243]/F')
        tree3.Branch('intch',intch,'intch[9]/F')
        tree3.Branch('fileid',fileid,'fileid/I')

        
        for fiid in range(filenamedf.shape[0]):
            if fiid < 15:
                relatedpixels=longimap[scanid:scanid+3,1:4].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,1:4].reshape(9)
            elif fiid < 33:
                relatedpixels=longimap[scanid:scanid+3,2:5].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,2:5].reshape(9)
            else:
                relatedpixels=longimap[scanid:scanid+3,3:6].reshape(9)
                relatednorm=normvalue[scanid:scanid+3,3:6].reshape(9)
                
            print(scanid,fiid)
            fileid[0]=fiid
            intarray=ReadSingleRawTxTReturnIntegral(filenamedf['scanstart'+str(longimap[scanid+1,2])].iloc[fiid],relatedpixels,relatednorm,Nbofevents,thisledch=ledch,thisbeamch=beamch)
            for itr in range(intarray.shape[0]):
                for k in range(9):
                    intch[k]=intarray[itr,k]
                if fiid <15:
                    tree1.Fill()
                elif fiid<33:
                    tree2.Fill()
                else:
                    tree3.Fill()
        f.Write()
        f.Close()
WriteTreeForEachScan()
