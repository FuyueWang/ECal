import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle
import warnings
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 

import architecture 
import dataclass
import trainmodel
import mynetwork

supdir='../../../data/nnx/tensorflow/'

def main():
    scan=0 #0,1
    row=2 #1,2,3
    # # specific parameters
    dataname=[supdir+'cnnwavescan'+str(scan)+'row'+str(row)+'.dat', 'data', 'label', 'label']
    testdataname=''
    # # CNN
    # modeldir=supdir+"CNNmodels"+str(scan)+'row'+str(row)+'/'
    # mynet=mynetwork.mycnnnetwork(dataname,modeldir,scan)


    modeldir=supdir+"CNNmodels"+str(scan)+'row'+str(row)+'/'
    mynet=mynetwork.mycnnnetwork2(dataname,modeldir,row)

    # lstm
    # modeldir=supdir+"LSTMmodels"+str(noi)+'/'
    # mynet=mynetwork.mylstmnetwork(dataname,modeldir,noi)
    
    # specific parameter
    # dataname=[supdir+'integralscan'+str(scan)+'.dat', 'data', 'label', 'label']

    # # DNN
    # modeldir=supdir+"DNNmodels"+str(scan)+'/'
    # mynet=mynetwork.mydnnnetwork(dataname,modeldir,scan)

    
    #  ----------------------------------------------------------------------#
    # in netowrk sessions. DO NOT CHANGE !!!!!!!!!!!!
    netarchitecture = architecture.architecture(dict(layer=mynet.cnnlayer,activation=mynet.cnnact),dict(layer=mynet.lstmlayer),dict(layer=mynet.dnnlayer,activation=mynet.dnnact))
    data = dataclass.dataclass(dataname,[mynet.trainsize,mynet.batchsize,mynet.validatesize],mynet.datadim, testdataname)
    training = trainmodel.trainmodel([mynet.startlearningrate, mynet.Nbofsaveriteractions, mynet.printiteractions, modeldir, mynet.Nboflearn, mynet.classificationthreshold], data, netarchitecture)
    training.train()
    # training.validate()
    #  ----------------------------------------------------------------------#

if __name__ == '__main__':
    # args = argsparser()
    main()
