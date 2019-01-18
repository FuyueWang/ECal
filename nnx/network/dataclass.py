import numpy as np
import pickle
class dataclass():
    """
    operactions with data

    This class contains all the parameters related with the training, validating and testing dataset.
    All the parameters are set outside this class! They are not supposed to be set here.

    fcn:
    GetTraindata(): returns the training data for the network
    Getvaldata(): returns the validating data for the network
    
    """
    def __init__(self, dataname='', dimpara=[], datadim=[], testdataname=''):
        self.trainsize = dimpara[0]
        self.batchsize = dimpara[1]
        self.validatesize = dimpara[2]
        self.Nbofbatch=self.trainsize//self.batchsize
        self.datadim = datadim #[imput dim0 dim1..., output dim]
        if dataname[0]=='':
            self.data= []
        else:    
            with open(dataname[0], 'rb') as f:
                self.data=pickle.load(f)
        self.featurename = dataname[1]
        self.labelitem = dataname[2]
        self.labelname = dataname[3]
        self.testdataname = testdataname
        # print(self.data[self.featurename].shape)
        
    def Gettraindata(self,startbatch=0):
        inputx = self.data[self.featurename][startbatch*self.batchsize:(startbatch+1)*self.batchsize,:].reshape([self.batchsize]+self.datadim[:-1])
        inputy = np.array(self.data[self.labelitem][self.labelname].iloc[startbatch*self.batchsize:(startbatch+1)*self.batchsize]).reshape(self.batchsize,1)
        return inputx, inputy

    def Getvaldata(self):
        valx = self.data[self.featurename][self.trainsize:self.trainsize+self.validatesize,:].reshape([self.validatesize]+self.datadim[:-1])
        valy = np.array(self.data[self.labelitem][self.labelname].iloc[self.trainsize:self.trainsize+self.validatesize]).reshape(self.validatesize,1)
        return valx, valy
    
    def Gettestdata(self,flag):
        with open(self.testdataname, 'rb') as f:
            datafromfile=pickle.load(f)
        testsize = datafromfile[self.featurename].shape[0]
        testx = datafromfile[self.featurename][:,800+flag:2200+flag].reshape([testsize]+self.datadim[:-1])
        return testx
