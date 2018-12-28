import matplotlib
import numpy as np
import pickle
import matplotlib.pyplot as plt
from array import array
import pandas as pd
import os.path

infiledir="../../data/ecalpos/txtdata/"
outfiledir="../../data/ecalpos/dfdata/"
Nboftower=[4,4]
towerpitch=[4,4] #cm
scanstep=[0.5,0.5] #cm

NbofscanID=4
scanID=[58,59,60,61]
startfileID=[172244,179926,183015,191430]
endfileID=[174724,182152,185151,194436]


longimap=[k for k in range(57,65)]
for k in range(49,57):
    longimap.append(k)
for k in reversed(range(1,9)):
    longimap.append(k)
for k in reversed(range(9,17)):
    longimap.append(k)    
longimap=np.array(longimap).reshape(4,8)



def Create3by3dataframe(startscan=0,endscan=3):
    for scanid in range(startscan,endscan+1):
        print("scan",scanid)
        fullIntdf=pd.DataFrame(columns=['IntCh0','IntCh1','IntCh2','IntCh3','IntCh4','IntCh5','IntCh6','IntCh7','IntCh8','centralTowerID','Nbof0pixel','Posy'])
        fullMaxdf=pd.DataFrame(columns=['MaxCh0','MaxCh1','MaxCh2','MaxCh3','MaxCh4','MaxCh5','MaxCh6','MaxCh7','MaxCh8','centralTowerID','Nbof0pixel','Posy'])
        Nboffile=0
        for fileid in range(startfileID[scanid],endfileID[scanid]+1):
            filename=infiledir+'076d3e83_20180824_'+str(fileid)+'.txt'
            if os.path.exists(filename):
                Nboffile+=1
                if Nboffile<11 or Nboffile>25 or Nboffile==18 : #
                    continue
                else:
                    centerTowerID=longimap[Nboffile//9,scanid+1]
                    print('file:',centerTowerID,Nboffile,filename)
                    filedict=ReadSingleRawTxtFile(filename,centerTowerID,longimap)
                    thisIntdf=pd.DataFrame(data=filedict['IntCHlist'],columns=['IntCh0','IntCh1','IntCh2','IntCh3','IntCh4','IntCh5','IntCh6','IntCh7','IntCh8'])
                    thisIntdf['centralTowerID']=[centerTowerID for k in range(len(filedict['ZeroPixelScore']))]
                    thisIntdf['Nbof0pixel']=filedict['ZeroPixelScore']
                    thisIntdf['Posy']=(Nboffile//9+0.5)*towerpitch[1]-(Nboffile-1)*scanstep[1]
                    
                    thisMaxdf=pd.DataFrame(data=filedict['MaxCHlist'],columns=['MaxCh0','MaxCh1','MaxCh2','MaxCh3','MaxCh4','MaxCh5','MaxCh6','MaxCh7','MaxCh8'])
                    thisMaxdf['centralTowerID']=[centerTowerID for k in range(len(filedict['ZeroPixelScore']))]
                    thisMaxdf['Nbof0pixel']=filedict['ZeroPixelScore']                   
                    thisMaxdf['Posy']=(Nboffile//9+0.5)*towerpitch[1]-(Nboffile-2)*scanstep[1]

                    fullIntdf=fullIntdf.append(thisIntdf)
                    fullMaxdf=fullMaxdf.append(thisMaxdf)
                    
        fullIntdf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'Intdf.csv')
        fullMaxdf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'Maxdf.csv')    

def ReadAndCheckPixelwiseDFFile():
    scanid=0
    Intdf=pd.read_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'Intdf.csv')
    
    fig = plt.figure(figsize=(10,10))
    for k in range(9):
        ax = plt.subplot2grid((3,3), (k//3,k%3))
        Intdf.hist('IntCh'+str(k),ax=ax)
    plt.show()

def ReadMaxData(filedir,startscan=2,endscan=3):
    Maxdf=pd.read_csv(filedir+'scanfrom'+str(scanID[startscan])+'Maxdf.csv')
    for k in range(startscan+1,endscan+1):
        Maxdf.append(pd.read_csv(filedir+'scanfrom'+str(scanID[k])+'Maxdf.csv'))

    # Maxdf['MaxCh0']=Maxdf['MaxCh0']/1000
    # Maxdf['MaxCh1']=Maxdf['MaxCh1']/1000
    # Maxdf['MaxCh2']=Maxdf['MaxCh2']/1000
    # Maxdf['MaxCh3']=Maxdf['MaxCh3']/1000
    # Maxdf['MaxCh4']=Maxdf['MaxCh4']/1000
    # Maxdf['MaxCh5']=Maxdf['MaxCh5']/1000
    # Maxdf['MaxCh6']=Maxdf['MaxCh6']/1000
    # Maxdf['MaxCh7']=Maxdf['MaxCh7']/1000
    # Maxdf['MaxCh8']=Maxdf['MaxCh8']/1000
        
    Maxdf['estimatepos']=((Maxdf['MaxCh0']+Maxdf['MaxCh1']+Maxdf['MaxCh2'])*4.-(Maxdf['MaxCh6']+Maxdf['MaxCh7']+Maxdf['MaxCh8'])*4.)/(Maxdf['MaxCh0']+Maxdf['MaxCh1']+Maxdf['MaxCh2']+Maxdf['MaxCh3']+Maxdf['MaxCh4']+Maxdf['MaxCh5']+Maxdf['MaxCh6']+Maxdf['MaxCh7']+Maxdf['MaxCh8'])
    return Maxdf

def ReadIntData(filedir,startscan=2,endscan=3):
    Intdf=pd.read_csv(filedir+'scanfrom'+str(scanID[startscan])+'Intdf.csv')
    for k in range(startscan+1,endscan+1):
        Intdf.append(pd.read_csv(filedir+'scanfrom'+str(scanID[k])+'Intdf.csv'))

    # Intdf['IntCh0']=Intdf['IntCh0']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh1']=Intdf['IntCh1']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh2']=Intdf['IntCh2']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh3']=Intdf['IntCh3']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh4']=Intdf['IntCh4']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh5']=Intdf['IntCh5']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh6']=Intdf['IntCh6']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh7']=Intdf['IntCh7']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    # Intdf['IntCh8']=Intdf['IntCh8']/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
        
    Intdf['estimatepos']=((Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2'])*4.-(Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])*4.)/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])
    return Intdf
    
def ReadSingleRawTxtFile(filename,centralTowerID,pixelmap=longimap):
    centralToweridex=np.where(pixelmap==centralTowerID)
    id1=centralToweridex[0][0]
    id2=centralToweridex[1][0]
    this3by3pixelsID=pixelmap[id1-1:id1+2,id2-1:id2+2].reshape(1,9)
    Intchannellist=[]
    Maxchannellist=[]
    Zeropixelscorelist=[]
    Intchannel=list(999*np.ones(9))
    Maxchannel=list(999*np.ones(9))
    zeropixelscore=[1,2,1,2,3,2,1,2,1]
    
    firstEvent=True
    with open(filename,'r') as f:
        lineid=0
        for line in f:
            lineid+=1
            if len(line.split()) > 0:
                line=line.split()
                if line[0]=="Event":
                    if firstEvent:
                        firstEvent=False
                    else:
                        # print("new event:",line)
                        Zeropixelscorelist.append(sum((np.array(Maxchannel)>998)*zeropixelscore))
                        Intchannel=list((np.array(Intchannel)<999)*Intchannel)
                        Maxchannel=list((np.array(Maxchannel)<999)*Intchannel)
                        Intchannellist.append(Intchannel)
                        Maxchannellist.append(Maxchannel)
                        Intchannel=list(999*np.ones(9))
                        Maxchannel=list(999*np.ones(9))
                else:
                    if int(line[0]) in this3by3pixelsID[0]:
                        if len(line[1:])>0:
                            Intchannel[np.where(this3by3pixelsID[0]==int(line[0]))[0][0]]=sum(list(map(int,line[1:])))
                            Maxchannel[np.where(this3by3pixelsID[0]==int(line[0]))[0][0]]=min(list(map(int,line[1:]))) #negative value, so we take min
            # if lineid>20:
            #     break
    return dict(IntCHlist=Intchannellist,MaxCHlist=Maxchannellist,ZeroPixelScore=Zeropixelscorelist)
    
            
def CheckFileName():
    for scanid in range(0,NbofscanID):
        print("scan",scanid)
        Nboffileid=0
        for fileid in range(startfileID[scanid],endfileID[scanid]+1):
            file_path=infiledir+'txtdata/076d3e83_20180824_'+str(fileid)+'.txt'
            if os.path.exists(file_path):
                Nboffileid=Nboffileid+1
                print(Nboffileid,file_path)

# Create3by3dataframe(0,1)
# scanid=0
# Intdf=pd.read_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'Intdf.csv')
    
def IntInterpolation():
    outdatadir="../../data/ecalpos/"
    Intdf=ReadData(outdatadir+'dfdata/',2,3) #pd.read_csv(outdatadir+'dfdata/'+'scanfrom'+str(scanID[scanid])+'Intdf.csv')
    Intdf.sample(frac=1)

    Intdf['estimatepos']=((Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2'])*4.-(Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])*4.)/(Intdf['IntCh0']+Intdf['IntCh1']+Intdf['IntCh2']+Intdf['IntCh3']+Intdf['IntCh4']+Intdf['IntCh5']+Intdf['IntCh6']+Intdf['IntCh7']+Intdf['IntCh8'])

    Intdf['residual']=Intdf['estimatepos']-Intdf['Posy']
    bins = np.linspace(-5, 5,100)
    plt.hist(Intdf['residual'],bins)
    plt.show()
    
def MaxInterpolation():
    outdatadir="../../data/ecalpos/"
    Maxdf=ReadMaxData(outdatadir+'dfdata/',2,3) #pd.read_csv(outdatadir+'dfdata/'+'scanfrom'+str(scanID[scanid])+'Maxdf.csv')
    Maxdf.sample(frac=1)

    Maxdf['estimatepos']=((Maxdf['MaxCh0']+Maxdf['MaxCh1']+Maxdf['MaxCh2'])*4.-(Maxdf['MaxCh6']+Maxdf['MaxCh7']+Maxdf['MaxCh8'])*4.)/(Maxdf['MaxCh0']+Maxdf['MaxCh1']+Maxdf['MaxCh2']+Maxdf['MaxCh3']+Maxdf['MaxCh4']+Maxdf['MaxCh5']+Maxdf['MaxCh6']+Maxdf['MaxCh7']+Maxdf['MaxCh8'])

    Maxdf['residual']=Maxdf['estimatepos']-Maxdf['Posy']
    print("mean:",Maxdf['residual'].mean(),"std:",Maxdf['residual'].std())
    plt.hist(Maxdf['residual'])
    plt.show()

# MaxInterpolation()

def CreateWaveformData(startscan=0,endscan=3):
    for scanid in range(startscan,endscan+1):
        print("scan",scanid)
        Nboffile=0
        waveformlist=[]
        poslist=[]
        for fileid in range(startfileID[scanid],endfileID[scanid]+1):
            filename=infiledir+'076d3e83_20180824_'+str(fileid)+'.txt'
            if os.path.exists(filename):
                Nboffile+=1
                if Nboffile<10 or Nboffile>24: #
                    continue
                else:
                    centerTowerID=longimap[Nboffile//9,scanid+1]   
                    print('file:',centerTowerID,Nboffile,filename)
                    thiswavefromlist=ReadSingleRawTxtFileWaveform(filename,centerTowerID,longimap)
                    waveformlist=waveformlist+thiswavefromlist
                    poslist=poslist+[(Nboffile//9+0.5)*towerpitch[1]-(Nboffile-1)*scanstep[1] for k in range(len(thiswavefromlist))]

        waveformnp=np.array(waveformlist)
        waveformnp.tofile(outfiledir+'scanfrom'+str(scanID[scanid])+'waveform.txt',np.array(waveformlist).reshape(1,np.array(waveformlist).size))
        # np.savetxt(outfiledir+'scanfrom'+str(scanID[scanid])+'waveform.txt',np.array(waveformlist).reshape(1,np.array(waveformlist).size))
        np.savetxt(outfiledir+'scanfrom'+str(scanID[scanid])+'label.txt',np.array(poslist))

                
def ReadSingleRawTxtFileWaveform(filename,centralTowerID,pixelmap=longimap):
    centralToweridex=np.where(pixelmap==centralTowerID)
    id1=centralToweridex[0][0]
    id2=centralToweridex[1][0]
    this3by3pixelsID=pixelmap[id1-1:id1+2,id2-1:id2+2].reshape(1,9)
    waveform=np.ones(540).reshape(9,60,1)
    waveformlist=[]
    
    firstEvent=True
    with open(filename,'r') as f:
        lineid=0
        for line in f:
            lineid+=1
            if len(line.split()) > 0:
                line=line.split()
                if line[0]=="Event":
                    if firstEvent:
                        firstEvent=False
                    else:
                        waveformlist.append(waveform)
                        waveform=np.ones(540).reshape(9,60,1)
                else:
                    if int(line[0]) in this3by3pixelsID[0]:
                        if len(line[1:])==60:
                            waveform[np.where(this3by3pixelsID[0]==int(line[0]))[0][0],:,0]=list(map(int,line[1:]))
            # if lineid>60:
            #     break
    return waveformlist
    
def ReadWaveform():
    scanid=0
    with open(outfiledir+'scanfrom'+str(scanID[scanid])+'waveform.dat', 'rb') as f:
        datafromfile = pickle.load(f)


def Create3by3dataframeSingledata(Nboffile):
    fullIntdf=pd.DataFrame(columns=['IntCh0','IntCh1','IntCh2','IntCh3','IntCh4','IntCh5','IntCh6','IntCh7','IntCh8','centralTowerID','Nbof0pixel','Posy'])
    fullMaxdf=pd.DataFrame(columns=['MaxCh0','MaxCh1','MaxCh2','MaxCh3','MaxCh4','MaxCh5','MaxCh6','MaxCh7','MaxCh8','centralTowerID','Nbof0pixel','Posy'])
    scanid=2
    if Nboffile==10:
        fileid=183711 #10
    elif Nboffile==11:
        fileid=183757 #11
    elif Nboffile==9:
        fileid=183641
    else:
        fileid=183552
    filename=infiledir+'076d3e83_20180824_'+str(fileid)+'.txt'
    centerTowerID=longimap[2,scanid+1]#[Nboffile//9,scanid+1]
    print('file:',centerTowerID,Nboffile,filename)
    filedict=ReadSingleRawTxtFile(filename,centerTowerID,longimap)
    thisIntdf=pd.DataFrame(data=filedict['IntCHlist'],columns=['IntCh0','IntCh1','IntCh2','IntCh3','IntCh4','IntCh5','IntCh6','IntCh7','IntCh8'])
    thisIntdf['centralTowerID']=[centerTowerID for k in range(len(filedict['ZeroPixelScore']))]
    thisIntdf['Nbof0pixel']=filedict['ZeroPixelScore']
    thisIntdf['Posy']=(Nboffile//9+0.5)*towerpitch[1]-(Nboffile-1)*scanstep[1]
    
    thisMaxdf=pd.DataFrame(data=filedict['MaxCHlist'],columns=['MaxCh0','MaxCh1','MaxCh2','MaxCh3','MaxCh4','MaxCh5','MaxCh6','MaxCh7','MaxCh8'])
    thisMaxdf['centralTowerID']=[centerTowerID for k in range(len(filedict['ZeroPixelScore']))]
    thisMaxdf['Nbof0pixel']=filedict['ZeroPixelScore']                   
    thisMaxdf['Posy']=(Nboffile//9+0.5)*towerpitch[1]-(Nboffile-2)*scanstep[1]
    
    fullIntdf=fullIntdf.append(thisIntdf)
    fullMaxdf=fullMaxdf.append(thisMaxdf)
    
    fullIntdf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'Intdf'+str(Nboffile)+'.csv')
    fullMaxdf.to_csv(outfiledir+'scanfrom'+str(scanID[scanid])+'Maxdf'+str(Nboffile)+'.csv')
    
def ReadSingleMaxData(filename):
    Maxdf=pd.read_csv(filename)
    
    Maxdf['estimatepos']=((Maxdf['MaxCh0']+Maxdf['MaxCh1']+Maxdf['MaxCh2'])*4.-(Maxdf['MaxCh6']+Maxdf['MaxCh7']+Maxdf['MaxCh8'])*4.)/(Maxdf['MaxCh0']+Maxdf['MaxCh1']+Maxdf['MaxCh2']+Maxdf['MaxCh3']+Maxdf['MaxCh4']+Maxdf['MaxCh5']+Maxdf['MaxCh6']+Maxdf['MaxCh7']+Maxdf['MaxCh8'])
    return Maxdf


def GetPixelMean(Nboffile):
    scanid=2
    filename=outfiledir+'scanfrom'+str(scanID[scanid])+'Maxdf'+str(Nboffile)+'.csv'
    Intdf=ReadSingleMaxData(filename)
    a=np.array([Intdf['MaxCh0'].mean(),Intdf['MaxCh1'].mean(),Intdf['MaxCh2'].mean(),Intdf['MaxCh3'].mean(),Intdf['MaxCh4'].mean(),Intdf['MaxCh5'].mean(),Intdf['MaxCh6'].mean(),Intdf['MaxCh7'].mean(),Intdf['MaxCh8'].mean()]).reshape(3,3)
    a=a/a[1,1]
    b=Intdf['Posy'].mean()
    return a,b


def CheckValueAbove0():
    outdatadir="../../data/ecalpos/"
    Intdf=ReadMaxData(outdatadir+'dfdata/',2,2)
    for k in range(Intdf.shape[0]):
        if Intdf['MaxCh4'].iloc[k]>0:
            print("k:",k,"Value:",Intdf['MaxCh4'].iloc[k])


pos=[1.5,1,0.5,0,-0.5,-1,-1.5]
def plotpixel(posID):
    bins=np.linspace(-300000,3000,100)
    plt.hist(Intdf[Intdf['Posy']>pos[posID]-0.1][Intdf['Posy']<pos[posID]+0.1]['dim0'],bins,histtype='step',label='top',linewidth=2)
    plt.hist(Intdf[Intdf['Posy']>pos[posID]-0.1][Intdf['Posy']<pos[posID]+0.1]['dim1'],bins,histtype='step',label='mid',linewidth=2)
    plt.hist(Intdf[Intdf['Posy']>pos[posID]-0.1][Intdf['Posy']<pos[posID]+0.1]['dim2'],bins,histtype='step',label='down',linewidth=2)
    plt.legend(loc='upper left',fontsize=15)
    plt.title('y='+str(pos[posID]))
    plt.savefig("../../plot/ecalpos/pixelID"+str(posID)+".png",dpi=200)
    plt.show()


