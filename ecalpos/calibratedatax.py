import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path
from decimal import *

infiledir="../../data/ecalpos/txtdata/"
outfiledir="../../data/ecalpos/dfdatax/"
outplotdir="../../plot/ecalpos/"
plottextsize=15
NbofscanID=2
scanID=[27,54]
startfileID=[140653,155051]
endfileID=[152923,172330]
tranmap=[k for k in range(58,64)]
for k in range(50,56):
    tranmap.append(k)
for k in range(26,32):
    tranmap.append(k)
for k in range(18,24):
    tranmap.append(k)    
tranmap=np.array(tranmap).reshape(4,6)

selectedmap=tranmap

def GetFileName():
    filenamelist=[]
    for scanid in range(2):
        thisid=0
        for fileid in range(startfileID[scanid],endfileID[scanid]+1):
            filename=infiledir+'076d3e83_20180825_'+str(fileid)+'.txt'
            if os.path.exists(filename):
                filenamelist.append(filename)
                thisid+=1
    filenamedataframe=pd.DataFrame({'scanstart27':filenamelist[0:50],'scanstart54':filenamelist[50:]})
    filenamedataframe.to_csv(outfiledir+'filename.csv')
    return filenamedataframe

def ReadDataAndExtract3by3PixelInfo():
    columnname=['ch'+str(k) for k in range(24)]+['fileid']
    
    filenamedf=pd.read_csv(outfiledir+'filename.csv')
    for scanid in range(2):
        pixelpd=pd.DataFrame(columns=columnname)
        for fiid in range(0,50):
            print('scanid',scanid,'fileid',fiid)
            filename=filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid]
            thispixelpd=ReadSingleRawTxtAndReturnEvery4by6PixelHist(filename,selectedmap)
            thispixelpd['col0']=thispixelpd['ch0']+thispixelpd['ch6']+thispixelpd['ch12']+thispixelpd['ch18']
            thispixelpd['col1']=thispixelpd['ch1']+thispixelpd['ch7']+thispixelpd['ch13']+thispixelpd['ch19']
            thispixelpd['col2']=thispixelpd['ch2']+thispixelpd['ch8']+thispixelpd['ch14']+thispixelpd['ch20']
            thispixelpd['col3']=thispixelpd['ch3']+thispixelpd['ch9']+thispixelpd['ch15']+thispixelpd['ch21']
            thispixelpd['col4']=thispixelpd['ch4']+thispixelpd['ch10']+thispixelpd['ch16']+thispixelpd['ch20']
            thispixelpd['col5']=thispixelpd['ch5']+thispixelpd['ch11']+thispixelpd['ch17']+thispixelpd['ch23']
            # print(thispixelpd.shape)
            mean=np.array(thispixelpd.mean())[24:]
            maxchannel=np.argmin(mean)
            # print('fileid',fiid,maxchannel)
            if maxchannel==0:
                thispixelpd=thispixelpd[thispixelpd['col'+str(maxchannel)]<mean[maxchannel]/20][thispixelpd['col'+str(maxchannel+1)]<mean[maxchannel+1]/2000]
            elif maxchannel==5:
                thispixelpd=thispixelpd[thispixelpd['col'+str(maxchannel)]<mean[maxchannel]/20][thispixelpd['col'+str(maxchannel-1)]<mean[maxchannel-1]/2000]
            else:
                thispixelpd=thispixelpd[thispixelpd['col'+str(maxchannel)]<mean[maxchannel]/20][thispixelpd['col'+str(maxchannel+1)]<mean[maxchannel+1]/2000][thispixelpd['col'+str(maxchannel-1)]<mean[maxchannel-1]/2000]
            thispixelpd=thispixelpd[['ch'+str(k) for k in range(24)]]

            thispixelpd['fileid']=np.ones(thispixelpd.shape[0])*fiid
            pixelpd=pixelpd.append(thispixelpd)
        pixelpd.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by6.csv')
    return pixelpd


def ReadSingleRawTxtAndReturnEvery4by6PixelHist(filename,selectedpixelmap):
    selectedpixelmap=selectedpixelmap.reshape(24)
    pixelrowvaluefor1event=np.zeros(24)
    pixelpd=pd.DataFrame(columns=['ch'+str(k) for k in range(24)])
    eventid=-1
    firstEvent=True
    with open(filename,'r') as f:
        for line in f:
            if len(line.split()) > 0:
                line=line.split()
                if line[0]=="Event":
                    eventid+=1
                    # print(line[1],"eve",eventid)
                    if firstEvent:
                        firstEvent=False
                    else:
                        pixelpd.loc[eventid]=pixelrowvaluefor1event
                        # print("print",pixelrowvaluefor1event)
                    pixelrowvaluefor1event=np.zeros(24)
                else:
                    if int(line[0]) in selectedpixelmap:
                        if len(line[1:])>0:
                            pixelarrayid=np.where(selectedpixelmap==int(line[0]))[0][0]
                            pixelrowvaluefor1event[pixelarrayid]=sum(list(map(int,line[1:])))
            # if eventid>100:
            #     break
        eventid+=1                 
        pixelpd.loc[eventid]=pixelrowvaluefor1event
    return pixelpd

def FindNormValueIndependent():
    filenamedf=pd.read_csv(outfiledir+'filename.csv')
    maxpixelvalue=np.zeros(8).reshape(2,4)
    for scanid in range(NbofscanID):
        relatedpixelscolumn=tranmap[1+scanid,2:6]
        maxpixellist=[]
        for fiid in range(0,50):
            print(scanid,fiid)
            maxpixellist.append(ReadSingleRawTxTforNormIndependent(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixelscolumn))
        maxpixelvalue[scanid,:]=np.array(maxpixellist).min(axis=0)
    np.savetxt(outfiledir+'normvalueinde.txt',maxpixelvalue)
    return maxpixelvalue
            

def ReadSingleRawTxTforNormIndependent(filename,relatedpixels):
    eventid=-1
    maxpixelvalue=list(np.zeros(4))
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
                            maxpixelvalue[pixelarrayid]=min(maxpixelvalue[pixelarrayid],sum(list(map(int,line[1:]))))
            # if eventid>1000:
            #     break
        eventid+=1                 
        maxpixelvalue[pixelarrayid]=min(maxpixelvalue[pixelarrayid],sum(list(map(int,line[1:]))))
    return maxpixelvalue

def Read4by6PixelData():
    scandf=[pd.read_csv(outfiledir+'scanfrom'+str(scanID[0])+'pixel4by6.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[1])+'pixel4by6.csv')]
    return scandf


def Extract3by3Usefuldata(startscanid=0,endscanid=0):
    for scanid in range(startscanid,endscanid+1):
        thisdfdata=norm4by6data[scanid].groupby
        





def CreateNormdata(startscanid,endscanid):
    columnname=['ch'+str(k) for k in range(24)]+['fileid']
    normvalue=np.loadtxt(outfiledir+'normvalueinde.txt')[:,1:7].reshape(24)
    for scanid in range(startscanid,endscanid+1):
        thisscandf=pixeldata4by6[scanid]
        for k in range(24):
            thisscandf['ch'+str(k)]=thisscandf['ch'+str(k)]/normvalue[k]
        thisscandf=thisscandf[columnname]
        thisscandf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by6norm.csv')
    

def ReadNorm4by6PixelData():
    normscandf=[pd.read_csv(outfiledir+'scanfrom'+str(scanID[0])+'pixel4by6norm.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[1])+'pixel4by6norm.csv')]
    return normscandf



def PlotPixelValueWithRespecttofileIDNorm(startscanid,endscanid):
    columnname=['ch'+str(k) for k in range(13,17)]+['ch'+str(k) for k in range(7,11)] #+['fileid']
    x=[k for k in range(50)]
    channelID=np.array(range(16)).reshape(4,4)
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=norm4by6data[scanid]
        pixelvaluethroughy=np.array(thisnormscandf.groupby('fileid').mean()[columnname])
        fig = plt.figure(figsize=(7,6))
        ax = plt.subplot2grid((1,1), (0,0))
        # plt.title(str(selectedmap[0,scanid+1]))
        plt.scatter(x,pixelvaluethroughy[:,scanid*4], label=str(tranmap[2-scanid,1]))
        plt.scatter(x,pixelvaluethroughy[:,scanid*4+1], label=str(tranmap[2-scanid,2]))
        plt.scatter(x,pixelvaluethroughy[:,scanid*4+2], label=str(tranmap[2-scanid,3]))
        plt.scatter(x,pixelvaluethroughy[:,scanid*4+3], label=str(tranmap[2-scanid,4]))
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize)    
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize) 
        plt.legend(loc='upper right',fontsize=plottextsize,ncol=4,labelspacing=0.1,handletextpad=0.05)
        plt.xlabel('File ID',fontsize=plottextsize)
        plt.ylabel('Pixel value',fontsize=plottextsize)
        plt.ylim([0, 0.8])
        plt.savefig(outplotdir+'pixelchangenorm'+str(scanid)+'x.png',dpi=200)
        plt.show()




# pixeldata4by6=Read4by6PixelData()
# CreateNormdata(0,0)
norm4by6data=ReadNorm4by6PixelData()





