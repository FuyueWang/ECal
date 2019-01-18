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
    scan=0
    # # specific parameters
    # dataname=[supdir+'cnnwavescan'+str(scan)+'.dat', 'data', 'label', 'label']
    testdataname=''
    # # CNN
    # modeldir=supdir+"CNNmodels"+str(scan)+'/'
    # mynet=mynetwork.mycnnnetwork(dataname,modeldir,scan)

    # lstm
    # modeldir=supdir+"LSTMmodels"+str(noi)+'/'
    # mynet=mynetwork.mylstmnetwork(dataname,modeldir,noi)
    
    # specific parameters
    dataname=[supdir+'integralscan'+str(scan)+'.dat', 'data', 'label', 'label']

    # DNN
    modeldir=supdir+"DNNmodels"+str(scan)+'/'
    mynet=mynetwork.mydnnnetwork(dataname,modeldir,scan)

    
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