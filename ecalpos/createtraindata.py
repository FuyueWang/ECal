# import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path
from ROOT import TFile, TTree
import ROOT as root
rootdir="../../data/ecalpos/rootdata/"
longimap=[k for k in range(57,65)]
for k in range(49,57):
    longimap.append(k)
for k in reversed(range(1,9)):
    longimap.append(k)
for k in reversed(range(9,17)):
    longimap.append(k)    
longimap=np.array(longimap).reshape(4,8)



def CheckNorm():
    columns=['pixel'+str(k) for k in range(4)]+['fileid']
    dflist=[]
    for scanid in range(1,2):
        centerpixeldf=pd.DataFrame(columns=columns)
        f = root.TFile(rootdir+"lwaveform"+str(scanid)+".root")
        intree = f.Get("wavetree")
        for entry in intree:
            centerpixeldf=centerpixeldf.append(pd.DataFrame(data=np.array([entry.intch[1],entry.intch[4],entry.intch[7],entry.intch[10],entry.fileid]).reshape(1,5),columns=columns))
        dflist.append(centerpixeldf.groupby('fileid').mean())
    # dflist.append(centerpixeldf)
    return dflist


def PlotCenterPixels(dflist):
    for scanid in range(1,2):
        fig = plt.figure(figsize=(7,6))
        ax = plt.subplot2grid((1,1), (0,0))
        plt.scatter(dflist[scanid-1].index,dflist[scanid-1].pixel0,label=str(longimap[0,scanid]))
        plt.scatter(dflist[scanid-1].index,dflist[scanid-1].pixel1,label=str(longimap[0,scanid]))
        plt.scatter(dflist[scanid-1].index,dflist[scanid-1].pixel2,label=str(longimap[0,scanid]))
        plt.scatter(dflist[scanid-1].index,dflist[scanid-1].pixel3,label=str(longimap[0,scanid]))
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize)    
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize) 
        plt.legend(loc='upper right',fontsize=plottextsize,ncol=4,labelspacing=0.1,handletextpad=0.05)
        plt.xlabel('File ID',fontsize=plottextsize)
        plt.ylabel('Pixel value',fontsize=plottextsize)
        # plt.ylim([0, 175000])
        plt.savefig(outplotdir+'pixelchange'+str(scanid)+'.png',dpi=200)
        plt.show()
        
PlotCenterPixels(CheckNorm())

def CheckNormWithRooT():
    columns=['pixel'+str(k) for k in range(4)]+['fileid']
    dflist=[]
    filex=np.array(range(33))
    for scanid in range(1,2):
        centerpixeldf=pd.DataFrame(columns=columns)
        f = root.TFile(rootdir+"lwaveform"+str(scanid)+".root")
        intree = f.Get("wavetree")
        intree.

        
        for entry in intree:
            centerpixeldf=centerpixeldf.append(pd.DataFrame(data=np.array([entry.intch[1],entry.intch[4],entry.intch[7],entry.intch[10],entry.fileid]).reshape(1,5),columns=columns))
        dflist.append(centerpixeldf.groupby('fileid').mean())
    # dflist.append(centerpixeldf)
    return dflist
