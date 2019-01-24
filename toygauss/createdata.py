import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import pickle
sigma=0.9
outdatadir='../../data/toygauss/tensorflow/'

channel=np.ones(4).reshape(1,4)
for poi in range(9):
    print(poi)
    mean=0.5*poi
    gaussvar=[random.gauss(mean,sigma) for k in range(10000000)]
    # plt.hist(distribution,bins=np.linspace(0,4,70))
    # plt.show()
    hist=plt.hist(gaussvar,bins=np.linspace(-6,10,400))
    gaussdis=hist[0]/1000000
    towerindex=[(hist[1]>-4).argmax(), (hist[1]>0).argmax(), (hist[1]>4).argmax(), (hist[1]>8).argmax()]
    
    channel1=np.array([random.gauss(0,0.1) for k in range(10000)]).reshape(10000,1)
    channel2=np.array([random.gauss(0,0.1) for k in range(10000)]).reshape(10000,1)
    channel3=np.array([random.gauss(0,0.1) for k in range(10000)]).reshape(10000,1)
    
    channel1=gaussdis[towerindex[0]:towerindex[1]].sum()+channel1
    channel2=gaussdis[towerindex[1]:towerindex[2]].sum()+channel2
    channel3=gaussdis[towerindex[2]:towerindex[3]].sum()+channel3

    channel=np.concatenate((channel,np.concatenate((channel1,channel2,channel3,np.ones(10000).reshape(10000,1)*mean),axis=1)),axis=0)
channel=channel[1:,:]
np.random.shuffle(channel)
dfcha=pd.DataFrame({'label': channel[:,-1]+0.5})
with open(outdatadir+'integra.dat', 'wb') as f:
    pickle.dump(dict(data=channel[:,:-1],label=dfcha), f)
