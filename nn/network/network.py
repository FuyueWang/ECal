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

supdir='../../../data/nn/tensorflow/'

def main():
    scan=5
    row=2
    # # specific parameters
    testdataname=''
    

    # CNN
    dataname=[supdir+'cnnwavescan'+str(scan)+'row'+str(row)+'.dat', 'data', 'label', 'label']
    modeldir=supdir+"CNNmodels"+str(scan)+'row'+str(row)+'/'
    mynet=mynetwork.mycnnnetwork(dataname,modeldir,scan)


    # # CNN
    # dataname=[supdir+'cnnwavescan'+str(scan)+'row'+str(row)+'.dat', 'data', 'label', 'label']
    # modeldir=supdir+"CNNmodels"+str(scan)+'row'+str(row)+'/'
    # mynet=mynetwork.mycnnnetwork2(dataname,modeldir,scan)

    
    # # lstm
    # dataname=[supdir+'wavescan'+str(scan)+'row'+str(row)+'.dat', 'data', 'label', 'label']
    # modeldir=supdir+"LSTMmodels"+str(scan)+'row'+str(row)+'/'
    # mynet=mynetwork.mylstmnetwork(dataname,modeldir,scan)
    
    # specific parameters
    

    # # DNN
    # dataname=[supdir+'integralscan'+str(scan)+'.dat', 'data', 'label', 'label']
    # modeldir=supdir+"DNNmodels"+str(scan)+'/'
    # mynet=mynetwork.mydnnnetwork(dataname,modeldir,scan)

    
    #  ----------------------------------------------------------------------#
    # in netowrk sessions. DO NOT CHANGE !!!!!!!!!!!!
    netarchitecture = architecture.architecture(dict(layer=mynet.cnnlayer,activation=mynet.cnnact),dict(layer=mynet.lstmlayer),dict(layer=mynet.dnnlayer,activation=mynet.dnnact))
    data = dataclass.dataclass(dataname,[mynet.trainsize,mynet.batchsize,mynet.validatesize],mynet.datadim, testdataname)
    training = trainmodel.trainmodel([mynet.startlearningrate, mynet.Nbofsaveriteractions, mynet.printiteractions, modeldir, mynet.Nboflearn, mynet.classificationthreshold], data, netarchitecture)
    # training.train()
    training.validate()
    #  ----------------------------------------------------------------------#

if __name__ == '__main__':
    # args = argsparser()
    main()
