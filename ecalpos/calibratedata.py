import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path
from decimal import *
# import scipy
# from scipy import ndimage
infiledir="../../data/ecalpos/txtdata/"
outfiledir="../../data/ecalpos/dfdata/"
outplotdir="../../plot/ecalpos/"
NbofscanID=8
scanID=[57,58,59,60,61,62,63,64]
startfileID=[164427,172244,175925,183015,191430,195325,202522,210502]
endfileID=[171339,174724,182152,185151,194436,201705,204706,212657]
plottextsize=15
longimap=[k for k in range(57,65)]
for k in range(49,57):
    longimap.append(k)
for k in reversed(range(1,9)):
    longimap.append(k)
for k in reversed(range(9,17)):
    longimap.append(k)    
longimap=np.array(longimap).reshape(4,8)

selectedmap=longimap

def GetFileName():
    filenamelist=[]
    for scanid in range(NbofscanID):
        for fileid in range(startfileID[scanid],endfileID[scanid]+1):
            filename=infiledir+'076d3e83_20180824_'+str(fileid)+'.txt'
            if os.path.exists(filename):
                filenamelist.append(filename)
    filenamedataframe=pd.DataFrame({'scanstart57':filenamelist[0:33],'scanstart58':filenamelist[33:66],'scanstart59':filenamelist[66:99],'scanstart60':filenamelist[99:132],'scanstart61':filenamelist[132:165],'scanstart62':filenamelist[165:198],'scanstart63':filenamelist[198:231],'scanstart64':filenamelist[231:]})
    filenamedataframe.to_csv(outfiledir+'filename.csv')
    return filenamedataframe
    
def Plotpostion(scanid,Nboffile):
    filenamedf=pd.read_csv(outfiledir+'filename.csv')
    filename=filenamedf['scanstart'+str(scanID[scanid])].iloc[Nboffile]
    rowspd,columnspd=ReadSingleRawTxtAndReturnPixelHist(filename,selectedmap)

    rowcolumnpd=pd.concat([rowspd,columnspd],axis=1,sort=False)
    mean=np.array(rowspd.mean())
    maxchannel=np.argmin(mean)

    columnmean=np.array(columnspd.mean())
    columnmaxchannel=np.argmin(columnmean)
    if maxchannel==0:
        rowcolumnpd=rowcolumnpd[rowcolumnpd['row'+str(maxchannel)]<mean[maxchannel]/20][rowcolumnpd['row'+str(maxchannel+1)]<mean[maxchannel+1]/2000]
        estimatepos=-mean[maxchannel+1]*4/(mean[maxchannel]+mean[maxchannel+1])
    elif maxchannel==3:
        rowcolumnpd=rowcolumnpd[rowcolumnpd['row'+str(maxchannel)]<mean[maxchannel]/20][rowcolumnpd['row'+str(maxchannel-1)]<mean[maxchannel-1]/2000]
        estimatepos=mean[maxchannel-1]*4/(mean[maxchannel-1]+mean[maxchannel])
    else:
        rowcolumnpd=rowcolumnpd[rowcolumnpd['row'+str(maxchannel)]<mean[maxchannel]/20][rowcolumnpd['row'+str(maxchannel+1)]<mean[maxchannel+1]/2000][rowcolumnpd['row'+str(maxchannel-1)]<mean[maxchannel-1]/2000]
        estimatepos=(mean[maxchannel-1]*4-mean[maxchannel+1]*4)/(mean[maxchannel-1]+mean[maxchannel]+mean[maxchannel+1])

    
    bins=np.linspace(-200000,3000,1000)
    fig = plt.figure(figsize=(10,7))
    ax = plt.subplot2grid((4,1), (0,0))
    plt.hist(rowcolumnpd['row0'],bins,histtype='step',label='1st row, mean='+str(mean[0]//1),linewidth=2)
    plt.legend(loc='upper left',fontsize=plottextsize)
    plt.title('ScanID:'+str(scanid)+', fileID:'+str(Nboffile)+',estimatePosy='+str(estimatepos),fontsize=plottextsize)
    plt.ylabel("Counts",fontsize=plottextsize,position=(0.8,0.93))
    ax = plt.subplot2grid((4,1), (1,0))
    plt.hist(rowcolumnpd['row1'],bins,histtype='step',label='2nd row mean='+str(mean[1]//1),linewidth=2)
    plt.legend(loc='upper left',fontsize=plottextsize)
    ax = plt.subplot2grid((4,1), (2,0))
    plt.hist(rowcolumnpd['row2'],bins,histtype='step',label='3rd row mean='+str(mean[2]//1),linewidth=2)
    plt.legend(loc='upper left',fontsize=plottextsize)
    ax = plt.subplot2grid((4,1), (3,0))
    plt.hist(rowcolumnpd['row3'],bins,histtype='step',label='4th row mean='+str(mean[3]//1),linewidth=2)
    plt.legend(loc='upper left',fontsize=plottextsize)
    plt.xlabel("Sum of value in 1 row",fontsize=plottextsize,position=(0.86,1))
    
    plt.savefig(outplotdir+'scan'+str(scanid)+'/file'+str(Nboffile)+'.png',dpi=200)
    # plt.show()

    fig2 = plt.figure(figsize=(10,7))
    plt.title('ScanID:'+str(scanid)+', fileID:'+str(Nboffile))
    for k in range(6):
        ax = plt.subplot2grid((1,6), (0,k))
        aplot=plt.hist(rowcolumnpd['column'+str(k)],bins,histtype='step',linewidth=2,orientation="horizontal") #,label=str(k+1)+', '+str(columnmean[k]//1)
        # ndimage.rotate(aplot, 90)
        # plt.legend(loc='lower left',fontsize=plottextsize-2,framealpha=1)
        if k==0:         
            plt.ylabel("Counts",fontsize=plottextsize,position=(0.8,0.93))
    plt.xlabel("Sum of value in 1 column",fontsize=plottextsize,position=(0.4,0.8))
    plt.savefig(outplotdir+'scan'+str(scanid)+'/file'+str(Nboffile)+'column.png',dpi=200)
    # plt.show()

    # return estimatepos #,rowcolumnpd

    
def ReadSingleRawTxtAndReturnPixelHist(filename,selectedpixelmap):
    rowspd=pd.DataFrame(columns=['row0','row1','row2','row3'])
    columnspd=pd.DataFrame(columns=['column0','column1','column2','column3','column4','column5'])
    selectedpixelmap=selectedpixelmap.reshape(24)
    
    firstEvent=True
    pixelrowvaluefor1event=np.zeros(4)
    pixelcolumnvaluefor1event=np.zeros(6)
    eventid=-1
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
                        rowspd.loc[eventid]=pixelrowvaluefor1event
                        columnspd.loc[eventid]=pixelcolumnvaluefor1event
                        # print("print",pixelvaluefor1event)
                    pixelrowvaluefor1event=np.zeros(4)
                    pixelcolumnvaluefor1event=np.zeros(6)
                else:
                    if int(line[0]) in selectedpixelmap:
                        if len(line[1:])>0:
                            pixelarrayid=np.where(selectedpixelmap==int(line[0]))[0][0]
                            pixelrowvaluefor1event[pixelarrayid//6]+=sum(list(map(int,line[1:])))
                            pixelcolumnvaluefor1event[pixelarrayid%6]+=sum(list(map(int,line[1:])))
                            # if eventid==26:
                            #     print(line[0],int(line[0]) in selectedpixelmap,pixelarrayid//6,sum(list(map(int,line[1:]))),pixelcolumnvaluefor1event)
            # if eventid>500:
            #     break
    return rowspd,columnspd



def ReadDataAndExtract3by3PixelInfo():
    columnname=['ch'+str(k) for k in range(32)]+['fileid']
    
    filenamedf=pd.read_csv(outfiledir+'filename.csv')
    for scanid in range(NbofscanID):
        pixelpd=pd.DataFrame(columns=columnname)
        for fiid in range(0,33):
            print('scanid',scanid,'fileid',fiid)
            filename=filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid]
            thispixelpd=ReadSingleRawTxtAndReturnEvery4by6PixelHist(filename,selectedmap)
            thispixelpd['row0']=thispixelpd['ch0']+thispixelpd['ch1']+thispixelpd['ch2']+thispixelpd['ch3']
            thispixelpd['row1']=thispixelpd['ch4']+thispixelpd['ch5']+thispixelpd['ch6']+thispixelpd['ch7']
            thispixelpd['row2']=thispixelpd['ch8']+thispixelpd['ch9']+thispixelpd['ch10']+thispixelpd['ch11']
            thispixelpd['row3']=thispixelpd['ch12']+thispixelpd['ch13']+thispixelpd['ch14']+thispixelpd['ch15']
            # print(thispixelpd.shape)
            mean=np.array(thispixelpd.mean())[16:]
            maxchannel=np.argmin(mean)
            # print('fileid',fiid,maxchannel)
            if maxchannel==0:
                thispixelpd=thispixelpd[thispixelpd['row'+str(maxchannel)]<mean[maxchannel]/20][thispixelpd['row'+str(maxchannel+1)]<mean[maxchannel+1]/2000]
            elif maxchannel==3:
                thispixelpd=thispixelpd[thispixelpd['row'+str(maxchannel)]<mean[maxchannel]/20][thispixelpd['row'+str(maxchannel-1)]<mean[maxchannel-1]/2000]
            else:
                thispixelpd=thispixelpd[thispixelpd['row'+str(maxchannel)]<mean[maxchannel]/20][thispixelpd['row'+str(maxchannel+1)]<mean[maxchannel+1]/2000][thispixelpd['row'+str(maxchannel-1)]<mean[maxchannel-1]/2000]
            thispixelpd=thispixelpd[['ch'+str(k) for k in range(16)]]

            
            thispixelpd['fileid']=[fiid for k in range(thispixelpd.shape[0])]
            pixelpd=pixelpd.append(thispixelpd)
        pixelpd.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4.csv')
    return pixelpd
            
def ReadSingleRawTxtAndReturnEvery4by6PixelHist(filename,selectedpixelmap):
    selectedpixelmap=selectedpixelmap[:,1:5].reshape(16)
    pixelrowvaluefor1event=np.zeros(16)
    pixelpd=pd.DataFrame(columns=['ch'+str(k) for k in range(16)])
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
                    pixelrowvaluefor1event=np.zeros(16)
                else:
                    if int(line[0]) in selectedpixelmap:
                        if len(line[1:])>0:
                            pixelarrayid=np.where(selectedpixelmap==int(line[0]))[0][0]
                            pixelrowvaluefor1event[pixelarrayid]=sum(list(map(int,line[1:])))
            # if eventid>1000:
            #     break
        eventid+=1                 
        pixelpd.loc[eventid]=pixelrowvaluefor1event
    return pixelpd


def FindNormValueIndependent():
    filenamedf=pd.read_csv(outfiledir+'filename.csv')
    maxpixelvalue=np.zeros(32).reshape(4,8)
    for scanid in range(NbofscanID):
        relatedpixelscolumn=longimap[:,scanid]
        maxpixellist=[]
        for fiid in range(0,33):
            print(scanid,fiid)
            maxpixellist.append(ReadSingleRawTxTforNormIndependent(filenamedf['scanstart'+str(scanID[scanid])].iloc[fiid],relatedpixelscolumn))
        maxpixelvalue[:,scanid]=np.array(maxpixellist).min(axis=0)
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



def FindNormValue(selectedpixelmap=selectedmap):
    selectedpixelmap=selectedpixelmap[:,1:5].reshape(16)
    pixelrowvaluefor1event=np.zeros(16)
    normmaxvalue=np.zeros(16).reshape(4,4)
    for scanid in range(0,4):
        channelId=np.array(range(16)).reshape(4,4)[:,scanid] #ChannelID of 60,52,5,13
        
        thisscandf=pixeldata4by4[scanid] #pd.read_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4.csv')
        selectcolumn=['ch'+str(channelId[k]) for k in range(4)]
        selectcolumn.append('fileid')
        thisscandf=thisscandf[selectcolumn]
        groupdf=pd.DataFrame(thisscandf.groupby('fileid').mean())
        normmaxvalue[:,scanid]=groupdf.min()
        np.savetxt(outfiledir+'normvalue.txt',normmaxvalue)
    return normmaxvalue
        


def CreateNormdata(startscanid,endscanid):
    columnname=['ch'+str(k) for k in range(16)]+['fileid']
    normvalue=np.loadtxt(outfiledir+'normvalue.txt').reshape(16)
    for scanid in range(startscanid,endscanid+1):
        thisscandf=pixeldata4by4[scanid]
        for k in range(16):
            thisscandf['ch'+str(k)]=thisscandf['ch'+str(k)]/normvalue[k]
        thisscandf=thisscandf[columnname]
        thisscandf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4norm.csv')


def ReadNorm4by4PixelData():
    normscandf=[pd.read_csv(outfiledir+'scanfrom'+str(scanID[0])+'pixel4by4norm.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[1])+'pixel4by4norm.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[2])+'pixel4by4norm.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[3])+'pixel4by4norm.csv')]
    return normscandf


def Read4by4PixelData():
    scandf=[pd.read_csv(outfiledir+'scanfrom'+str(scanID[0])+'pixel4by4.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[1])+'pixel4by4.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[2])+'pixel4by4.csv'),pd.read_csv(outfiledir+'scanfrom'+str(scanID[3])+'pixel4by4.csv')]
    return scandf



def CreateInterpolationData(startscanid=1,endscanid=2):
    columnname=['ch'+str(k) for k in range(16)]
    filex=[k for k in range(33)]
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=norm4by4pixeldata[scanid]
        centerpixelforeveryfile=np.array(thisnormscandf.groupby('fileid').mean()[columnname]).argmax(axis=1)
        dfest=pd.DataFrame(columns=['estimatePosy','fileestPosy'])
        for fiid in range(33):
            centerch=centerpixelforeveryfile[fiid]
            # print('scanid',scanid,'fileid:',fiid,'center:',centerch)
            if centerch<4:
                tmpdf=-(thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+3)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+5)])*4/(thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-1)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+1)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+3)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+5)])
            elif centerch>11:
                tmpdf=(thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-5)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-3)])*4/(thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-5)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-3)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-1)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+1)])
            else:
                tmpdf=(thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-5)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-3)]-thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+3)]-thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+4)]-thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+5)])*4/(thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-5)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-3)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch-1)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+1)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+3)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+4)]+thisnormscandf[thisnormscandf['fileid']==fiid]['ch'+str(centerch+5)])
  
            dfest=dfest.append(pd.DataFrame({'estimatePosy':tmpdf,'fileestPosy':tmpdf.mean()*np.ones(tmpdf.shape[0])}))
        
        thisnormscandf['estimatePosy']=dfest['estimatePosy']
        thisnormscandf['fileestPosy']=dfest['fileestPosy']
        
        thisnormscandf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4withestimatePosy.csv')

def CreateTrainData(startscanid=1,endscanid=2):
    standposy=[1.5,1,0.5,0,-0.5,-1,-1.5,1.5,1,0.5,0,-0.5,-1]
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=normpixelwithinterresult[scanid]
        thisnormscandf=thisnormscandf[thisnormscandf['fileid'].isin([k for k in range(8,15)]+[k for k in range(16,22)])]
        counts=list(thisnormscandf.groupby('fileid').count()['ch0'])
        posy=[]
        for k in range(len(counts)):
            posy+=list(standposy[k]*np.ones(counts[k]))
        thisnormscandf['standardPosy']=posy

        thisnormscandf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4withtrainPosy.csv')

def CreateInterpolationDataIn1Coord(startscanid=0,endscanid=3):
    columnname=['ch'+str(k) for k in range(16)]
    filex=[k for k in range(33)]
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=norm4by4pixeldata[scanid]
        thisnormscandf['Posyin1coord']=((thisnormscandf['ch0']+thisnormscandf['ch1']+thisnormscandf['ch2']+thisnormscandf['ch3'])*14+(thisnormscandf['ch4']+thisnormscandf['ch5']+thisnormscandf['ch6']+thisnormscandf['ch7'])*10+(thisnormscandf['ch8']+thisnormscandf['ch9']+thisnormscandf['ch10']+thisnormscandf['ch11'])*6+(thisnormscandf['ch12']+thisnormscandf['ch13']+thisnormscandf['ch14']+thisnormscandf['ch15'])*2)/(thisnormscandf['ch0']+thisnormscandf['ch1']+thisnormscandf['ch2']+thisnormscandf['ch3']+thisnormscandf['ch4']+thisnormscandf['ch5']+thisnormscandf['ch6']+thisnormscandf['ch7']+thisnormscandf['ch8']+thisnormscandf['ch9']+thisnormscandf['ch10']+thisnormscandf['ch11']+thisnormscandf['ch12']+thisnormscandf['ch13']+thisnormscandf['ch14']+thisnormscandf['ch15'])       
        thisnormscandf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4withestimatePosy1Coord.csv')

def ReadInterin1Coord(startscanid=0,endscanid=3):
    result=[]
    for scanid in range(startscanid,endscanid+1):
        result.append(pd.read_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'pixel4by4withestimatePosy1Coord.csv'))
    return result
        
def ReadNorm4by4WithInterResult():
    interresult=['',pd.read_csv(outfiledir+'scanfrom'+str(scanID[1])+'pixel4by4withestimatePosy.csv'), pd.read_csv(outfiledir+'scanfrom'+str(scanID[2])+'pixel4by4withestimatePosy.csv'),'']
    return interresult


def ReadTrainDatastudyinteraslabel(scanid=[2]):
    tmpdf=pd.DataFrame()
    tmpdf1=pd.DataFrame()
    readdf=pd.read_csv(outfiledir+'scanfrom'+str(scanID[2])+'pixel4by4withestimatePosy.csv')

    tmpdf['ch0']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch1']
    tmpdf['ch1']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch2']
    tmpdf['ch2']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch3']
    tmpdf['ch3']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch5']
    tmpdf['ch4']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch6']
    tmpdf['ch5']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch7']
    tmpdf['ch6']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch8']
    tmpdf['ch7']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch10']
    tmpdf['ch8']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['ch11']
    tmpdf['Posy']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['fileestPosy']
    tmpdf['estPosy']=readdf[readdf['fileid'].isin([k for k in range(8,15)])]['estimatePosy']

    tmpdf1['ch0']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch5']
    tmpdf1['ch1']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch6']
    tmpdf1['ch2']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch7']
    tmpdf1['ch3']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch9']
    tmpdf1['ch4']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch10']
    tmpdf1['ch5']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch11']
    tmpdf1['ch6']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch13']
    tmpdf1['ch7']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch14']
    tmpdf1['ch8']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['ch15']
    tmpdf1['Posy']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['fileestPosy']
    tmpdf1['estPosy']=readdf[readdf['fileid'].isin([k for k in range(15,22)])]['estimatePosy']
    traindf=tmpdf.append(tmpdf1)
    traindf=traindf.sample(frac=1).reset_index()
    return traindf

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


def ReadClassTrainData(scanid=[1]):
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

    labelmap={8:[0,0,0,0,0,0,0],9:[0,1,0,0,0,0,0],10:[0,0,1,0,0,0,0],11:[0,0,0,1,0,0,0],12:[0,0,0,0,1,0,0],13:[0,0,0,0,0,1,0],14:[0,0,0,0,0,0,1],16:[0,0,0,0,0,0,0],17:[0,1,0,0,0,0,0],18:[0,0,1,0,0,0,0],19:[0,0,0,1,0,0,0],20:[0,0,0,0,1,0,0],21:[0,0,0,0,0,1,0],22:[0,0,0,0,0,0,1]}
    traindf['label']=traindf['fileid'].map(labelmap)
    
    return traindf



def PlotPixelValueWithRespecttofileIDNorm(startscanid,endscanid):
    columnname=['ch'+str(k) for k in range(16)] #+['fileid']
    x=[k for k in range(33)]
    channelID=np.array(range(16)).reshape(4,4)
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=norm4by4pixeldata[scanid]
        pixelvaluethroughy=np.array(thisnormscandf.groupby('fileid').mean()[columnname])
        fig = plt.figure(figsize=(7,6))
        ax = plt.subplot2grid((1,1), (0,0))
        # plt.title(str(selectedmap[0,scanid+1]))
        plt.scatter(x,pixelvaluethroughy[:,channelID[0,scanid]], label=str(longimap[0,scanid+1]))
        plt.scatter(x,pixelvaluethroughy[:,channelID[1,scanid]], label=str(longimap[1,scanid+1]))
        plt.scatter(x,pixelvaluethroughy[:,channelID[2,scanid]], label=str(longimap[2,scanid+1]))
        plt.scatter(x,pixelvaluethroughy[:,channelID[3,scanid]], label=str(longimap[3,scanid+1]))
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize)    
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize) 
        plt.legend(loc='upper right',fontsize=plottextsize,ncol=4,labelspacing=0.1,handletextpad=0.05)
        plt.xlabel('File ID',fontsize=plottextsize)
        plt.ylabel('Pixel value',fontsize=plottextsize)
        plt.ylim([0, 1.2])
        plt.savefig(outplotdir+'pixelchangenorm'+str(scanid)+'.png',dpi=200)
        plt.show()

def PlotPixelValueWithRespecttofileID(startscanid,endscanid):
    columnname=['ch'+str(k) for k in range(16)] #+['fileid']
    x=[k for k in range(33)]
    channelID=np.array(range(16)).reshape(4,4)
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=pixeldata4by4[scanid]
        pixelvaluethroughy=np.array(thisnormscandf.groupby('fileid').mean()[columnname])
        fig = plt.figure(figsize=(7,6))
        ax = plt.subplot2grid((1,1), (0,0))
        # plt.title(str(selectedmap[0,scanid+1]))
        plt.scatter(x,-pixelvaluethroughy[:,channelID[0,scanid]], label=str(longimap[0,scanid+1]))
        plt.scatter(x,-pixelvaluethroughy[:,channelID[1,scanid]], label=str(longimap[1,scanid+1]))
        plt.scatter(x,-pixelvaluethroughy[:,channelID[2,scanid]], label=str(longimap[2,scanid+1]))
        plt.scatter(x,-pixelvaluethroughy[:,channelID[3,scanid]], label=str(longimap[3,scanid+1]))
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize)    
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(plottextsize) 
        plt.legend(loc='upper right',fontsize=plottextsize,ncol=4,labelspacing=0.1,handletextpad=0.05)
        plt.xlabel('File ID',fontsize=plottextsize)
        plt.ylabel('Pixel value',fontsize=plottextsize)
        plt.ylim([0, 175000])
        plt.savefig(outplotdir+'pixelchange'+str(scanid)+'.png',dpi=200)
        plt.show()

        
def PlotEstimateResult(startscanid=1,endscanid=2):
    listestimatemeanpos=[]
    listresidual=[]
    filex=[k for k in range(33)]
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=normpixelwithinterresult[scanid]
        fileestimate=np.array(thisnormscandf.groupby('fileid').mean()['fileestPosy'])
        residual=np.array(thisnormscandf['estimatePosy']-thisnormscandf['fileestPosy'])
        listestimatemeanpos.append(fileestimate)
        listresidual.append(residual)
    
    fig = plt.figure(figsize=(10,10))
    bins=np.linspace(-2, 2,100)
    plt.hist(listresidual[0],bins=bins,histtype='step', label='59,51,6,14,std='+str(Decimal(np.nanstd(listresidual[0])).quantize(Decimal('0.00')))+'cm',linewidth=2)
    plt.hist(listresidual[1],bins=bins,histtype='step', label='60,52,5,13,std='+str(Decimal(np.nanstd(listresidual[1])).quantize(Decimal('0.00')))+'cm',linewidth=2)
    plt.legend(loc='upper left',fontsize=plottextsize)
    plt.xlabel("residual [cm]",fontsize=plottextsize)
    plt.ylabel("Counts",fontsize=plottextsize)
    plt.legend(loc='upper right',fontsize=plottextsize)
    plt.show()

    fig1 = plt.figure(figsize=(10,10))
    bins=np.linspace(-2, 2,100)
    plt.scatter(filex,listestimatemeanpos[0],label='59,51,6,14')
    plt.scatter(filex,listestimatemeanpos[1],label='59,51,6,14')
    plt.show()

    return listestimatemeanpos

def PlotPosyin1coord(startscanid=0,endscanid=3):
    filex=[k for k in range(33)]
    fig1 = plt.figure(figsize=(7,6))
    ax = plt.subplot2grid((1,1), (0,0))
    for scanid in range(startscanid,endscanid+1):
        thisnormscandf=interdatain1coord[scanid]
        posy=np.array(thisnormscandf.groupby('fileid').mean()['Posyin1coord'])
        plt.scatter(filex,posy,label=str(longimap[0,1+scanid])+","+str(longimap[1,1+scanid])+","+str(longimap[2,1+scanid])+","+str(longimap[3,1+scanid]))
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(plottextsize)    
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(plottextsize) 
    plt.legend(loc='upper right',fontsize=plottextsize,handletextpad=0.05)
    plt.xlabel('File ID',fontsize=plottextsize)
    plt.ylabel('Position [cm]',fontsize=plottextsize)
    plt.ylim([0, 16])
    plt.grid()
    plt.savefig(outplotdir+"PlotPosyin1coord.png",dpi=200)
    plt.show()


def PlotInterResidual():
    fig1 = plt.figure(figsize=(7,6))
    ax = plt.subplot2grid((1,1), (0,0))
    bins=np.linspace(-2, 2,100)
    plt.hist(traindata[traindata['fileid'].isin([k for k in range(8,15)])].interPosy-traindata[traindata['fileid'].isin([k for k in range(8,15)])].standPosy,bins=bins,histtype='step',linewidth=2)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(plottextsize)    
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(plottextsize) 
    plt.text(0.5,0.5,"\sigma(y)="+str(Decimal((traindata.interPosy-traindata.standPosy).std()).quantize(Decimal('0.00'))),fontsize=plottextsize)
    plt.xlabel("Residual [cm]",fontsize=plottextsize)
    plt.ylabel("Counts",fontsize=plottextsize)
    plt.show()
    
# # readRawdata save as 4by4.csv
# ReadDataAndExtract3by3PixelInfo()

# print('read the pixel info data')
# # read the data created by last step for every scan
# pixeldata4by4=Read4by4PixelData()

# # print("Find norm value")
# # # Find the Norm Value of every Pixel and save that
# # FindNormValue()

# # print("Create norm data")
# # # Create the norm data save as 4by4norm.csv
# # CreateNormdata(0,3)

# print("read norm data")
# Read the norm data created by last step for every scan
# norm4by4pixeldata=ReadNorm4by4PixelData()

# print("create interpolation data")
# # Create the intepolation result, and save as pixel4by4withestimatePosy
# CreateInterpolationData()

# print("read interpolation data")
# # Read the interpolation data created by last step for every scan
# normpixelwithinterresult=ReadNorm4by4WithInterResult()

# # Create the interpolation result in 1 coordinate
# print("create interpolation data in 1 Coordinate")
# CreateInterpolationDataIn1Coord()

# print("read interpolation data in 1 Coordinate")
# interdatain1coord=ReadInterin1Coord()


# print("plot pixel value")
# # plot the pixel value 
# PlotPixelValueWithRespecttofileID(0,0)

# print("plot estimate value")
# # Plot the estimate posy result from the interpolation
# a=PlotEstimateResult()

# # plot the posy in 1 coordinate
# print("plot the posy in 1 coordinate")
# PlotPosyin1coord()

# print('create train data')
# CreateTrainData()

# print('read train data')
# traindata = ReadTrainData()
