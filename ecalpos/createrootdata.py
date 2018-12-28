
import numpy as np
import pickle

from array import array
import pandas as pd
# from calibratedata import ReadTrainData
from ROOT import TFile, TTree
scanID=[58,59,60,61]
outfiledir="../../data/ecalpos/dfdata/"
def ReadTrainData(scanid=[1]):
    tmpdf=pd.DataFrame()
    tmpdf1=pd.DataFrame()
    readdf=pd.read_csv(outfiledir+'scanfrom'+str(scanID[2])+'pixel4by4withtrainPosy.csv')
    tmpdf['ch0']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch1']
    tmpdf['ch1']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch2']
    tmpdf['ch2']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch3']
    tmpdf['ch3']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch5']
    tmpdf['ch4']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch6']
    tmpdf['ch5']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch7']
    tmpdf['ch6']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch8']
    tmpdf['ch7']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch10']
    tmpdf['ch8']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch11']
    tmpdf['interPosy']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['estimatePosy']
    tmpdf['standPosy']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['standardPosy']
    tmpdf['fileid']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['fileid']
    tmpdf1['ch0']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch5']
    tmpdf1['ch1']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch6']
    tmpdf1['ch2']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch7']
    tmpdf1['ch3']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch9']
    tmpdf1['ch4']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch10']
    tmpdf1['ch5']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch11']
    tmpdf1['ch6']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch13']
    tmpdf1['ch7']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch14']
    tmpdf1['ch8']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['ch15']
    tmpdf1['interPosy']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['estimatePosy']
    tmpdf1['standPosy']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['standardPosy']
    tmpdf1['fileid']=readdf[readdf['fileid'].isin([k for k in range(16,22)])]['fileid']
    traindf=tmpdf.append(tmpdf1)
    traindf=traindf.sample(frac=1).reset_index()
    return traindf

traindf=ReadTrainData()
outdatadir="../../data/ecalpos/"

f = TFile(outdatadir+"rootdata/train1.root", 'recreate' )
tree = TTree( 'traintree', 'traintree' )

pixelvalue= array('f',9*[0.])
posy= array('f',[0])
intposy=array('f',[0])
fileid=array('f',[0])
tree.Branch('pixelvalue',pixelvalue,'pixelvalue[9]/F')
tree.Branch('posy',posy,'posy/F')
tree.Branch('intposy',intposy,'intposy/F')
tree.Branch('fileid',fileid,'fileid/F')
for i in range(traindf.shape[0]):
    if traindf['standPosy'].iloc[i]>-1.51 and traindf['standPosy'].iloc[i]<1.51:
        posy[0]=traindf['standPosy'].iloc[i]
        intposy[0]=traindf['interPosy'].iloc[i]
        fileid[0]=traindf['fileid'].iloc[i]
        for k in range(9):
            pixelvalue[k]=traindf['ch'+str(k)].iloc[i]
        tree.Fill()

f.Write()
f.Close()
