# import matplotlib
import numpy as np
import pickle
# import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path
from ROOT import TFile, TTree

textdir="../../data/ecalpos/txtdata/"
dfdir="../../data/ecalpos/dfdata/"
rootdir="../../data/ecalpos/rootdata/"
NbofscanID=8
scanID=[57,58,59,60,61,62,63,64]
startfileID=[164427,172244,175925,183015,191430,195325,202522,210502]
endfileID=[171339,174724,182152,185151,194436,201705,204706,212657]

longimap=[k for k in range(57,65)]
for k in range(49,57):
    longimap.append(k)
for k in reversed(range(1,9)):
    longimap.append(k)
for k in reversed(range(9,17)):
    longimap.append(k)    
longimap=np.array(longimap).reshape(4,8)

def WriteTreeForEachScan():
    filenamedf=pd.read_csv(dfdir+'filename.csv')
    normvalue=np.loadtxt(dfdir+'normvalueinde.txt')

    wavech = array('f',720*[0.])
    intch = array('f',12*[0.])
    fileid = array('i',[0])

    for scanid in range(1,NbofscanID-1):
        relatedpixels=longimap[:,scanid-1:scanid+2].reshape(12)
        relatednorm=normvalue[:,scanid-1:scanid+2].reshape(12)
        f = TFile(rootdir+"lwaveform"+str(scanid)+".root", 'recreate' )
        tree = TTree( 'wavetree', 'wavetree' )
        tree.Branch('wavech',wavech,'wavech[720]/F')
        tree.Branch('intch',intch,'intch[12]/F')
        tree.Branch('fileid',fileid,'fileid/I')
        for fiid in range(0,33):
            print(scanid,fiid)
            fileid[0]=fiid
            wavelist,intlist=ReadSingleRawText(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixels,relatednorm)
            for itr in range(len(intlist)):
                for k in range(12):
                    intch[k]=intlist[itr][k]
                for k in range(720):
                    wavech[k]=wavelist[itr][k]
                tree.Fill()
                
        f.Write()
        f.Close()

def ReadSingleRawText(filename,relatedpixels,relatednorm):
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
                        wavelist.append(list(pixelwave.reshape(12*60)))
                        intlist.append(list(pixelint))
                    pixelwave=np.zeros(12*60).reshape(12,60)
                    pixelint=np.zeros(12)
                else:
                    if int(line[0]) in relatedpixels:
                        if len(line[1:])==60:
                            pixelarrayid=np.where(relatedpixels==int(line[0]))[0][0]
                            pixelwave[pixelarrayid,:]=np.array(map(int,line[1:]))/relatednorm[pixelarrayid]
                            pixelint[pixelarrayid]=sum(list(map(int,line[1:])))/relatednorm[pixelarrayid]
            # if eventid>10:
            #     break
        wavelist.append(list(pixelwave.reshape(12*60)))
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
















FindNormValueIndependent()
WriteTreeForEachScan()
        
