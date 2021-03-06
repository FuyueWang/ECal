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

supdir='../../../data/dubnann/tensorflow/'

def main():
    scan=5 #0-5
    row=1
    # # specific parameters
    testdataname=''
    

    # CNN
    dataname=[supdir+'cnnwavescan'+str(scan)+'.dat', 'data', 'label', 'label']
    modeldir=supdir+"CNNmodels"+str(scan)+'/'
    mynet=mynetwork.mycnnnetwork1(dataname,modeldir,scan)

    # # CNN
    # dataname=[supdir+'cnnwavescan'+str(scan)+'.dat', 'data', 'label', 'label']
    # modeldir=supdir+"CNNmodels"+str(scan)+'/'
    # mynet=mynetwork.mycnnnetwork3(dataname,modeldir,scan)

    
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
    training.validate('valpred.csv')
    #  ----------------------------------------------------------------------#

if __name__ == '__main__':
    # args = argsparser()
    main()
