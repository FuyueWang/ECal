import tensorflow as tf
# class mynetwork:
#     @abstractmethod
#     def __init__(self,):


class mycnnnetwork():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=250000
        self.batchsize=5000 
        self.validatesize=50000 
        
        self.datadim=[9,9,3,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.001
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 10000
        self.printiteractions = 100
        self.Nboflearn= 4

        if flag<7:
            self.cnnlayer=[32,32,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[10,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]
        elif flag==8:
            self.cnnlayer=[32,32,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.relu]
        if flag==30:
            self.validatesize=30000 
        self.lstmlayer=[]

class mycnnnetwork1():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=250000
        self.batchsize=10000 
        self.validatesize=50000 
        
        self.datadim=[9,9,3,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.0005
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 15000
        self.printiteractions = 100
        self.Nboflearn= 3

        if flag<7:
            self.cnnlayer=[24,32,64,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[10,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]
        elif flag==8:
            self.cnnlayer=[32,32,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.relu]
        if flag==30:
            self.validatesize=30000 
        self.lstmlayer=[]



class mylstmnetwork():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=25000
        self.batchsize=5000 
        self.validatesize=40000 
        
        self.datadim=[27,9,1] #[imput dim0 dim1..., output dim] [time_steps,n_input]

        self.startlearningrate= 0.01
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 5000
        self.printiteractions = 100
        self.Nboflearn= 3

        if flag<7:
            self.lstmlayer=[150]
            self.dnnlayer=[10,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]
        elif flag==8:
            self.lstmlayer=[100]
            self.dnnlayer=[5,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]           
                  
    
        self.cnnlayer=[]
        self.cnnact=[]

#processing the input tensor from [batch_size,n_steps,n_input] to "time_steps" number of [batch_size,n_input] tensors
class mydnnnetwork():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=180000
        self.batchsize=10000 
        self.validatesize=50000 
        
        self.datadim=[9,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.005
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 10000
        self.printiteractions = 500
        self.Nboflearn= 3

        if flag<7:
            self.dnnlayer=[9,10,14,20,5,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
        elif flag==8:
            self.dnnlayer=[9,10,14,20,5,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.relu]

        self.lstmlayer=[]
        self.cnnlayer=[]
        self.cnnact=[]
