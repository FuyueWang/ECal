import tensorflow as tf
# class mynetwork:
#     @abstractmethod
#     def __init__(self,):


class mycnnnetwork():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=60000
        self.batchsize=12000 
        self.validatesize=60000 
        
        self.datadim=[9,9,3,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.001
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 5000
        self.printiteractions = 80
        self.Nboflearn= 3
        
        if flag<7:
            self.cnnlayer=[30,62,70]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
        elif flag==20:
            self.cnnlayer=[32,64,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[10,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]
        if flag==30:
            self.validatesize=33000 
        self.lstmlayer=[]
        

class mycnnnetwork1():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=60000
        self.batchsize=6000 
        self.validatesize=100000 
        
        self.datadim=[9,9,3,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.001
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 20000
        self.printiteractions = 100
        self.Nboflearn= 3
        if flag==1:
            self.cnnlayer=[32,64,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.relu]
        elif flag==2 or flag==3:
            self.cnnlayer=[32,64]
            self.cnnact=[tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.relu]

        self.lstmlayer=[]
        
class mycnnnetwork2():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=60000
        self.batchsize=12000 
        self.validatesize=60000 
        
        self.datadim=[9,9,3,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.001
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 5000
        self.printiteractions = 80
        self.Nboflearn= 3
        
        if flag<7:
            self.cnnlayer=[12,32,64,80]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
        elif flag==20:
            self.cnnlayer=[32,64,64]
            self.cnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
            self.dnnlayer=[10,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]
        if flag==30:
            self.validatesize=33000 
        self.lstmlayer=[]
        
class mylstmnetwork():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=30000
        self.batchsize=6000 
        self.validatesize=9290 
        
        self.datadim=[70,20,1] #[imput dim0 dim1..., output dim] [time_steps,n_input]

        self.startlearningrate= 0.001
        self.classificationthreshold = 0.5 # set to be 999 for regression
        self.Nbofsaveriteractions = 5000
        self.printiteractions = 500
        self.Nboflearn=2

        if flag<4:
            self.lstmlayer=[150]
            self.dnnlayer=[10,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]
        elif flag==4:
            self.lstmlayer=[100]
            self.dnnlayer=[5,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]           
        elif flag==5:
            self.lstmlayer=[70]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]           
        elif flag==6:
            self.lstmlayer=[40]
            self.dnnlayer=[self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.relu]            
    
        self.cnnlayer=[]
        self.cnnact=[]

#processing the input tensor from [batch_size,n_steps,n_input] to "time_steps" number of [batch_size,n_input] tensors
class mydnnnetwork():
    """
    define every specific network
    """
    def __init__(self,dataname,modeldir,flag):
        self.trainsize=60000
        self.batchsize=12000 
        self.validatesize=100000 
        
        self.datadim=[9,1] #[imput dim0 dim1..., output dim]

        self.startlearningrate= 0.005
        self.classificationthreshold = 999 # set to be 999 for regression
        self.Nbofsaveriteractions = 50000
        self.printiteractions = 500
        self.Nboflearn= 3

        if flag==0:
            self.dnnlayer=[9,10,14,20,5,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.relu]
        elif flag==1:
            self.dnnlayer=[9,10,14,20,5,self.datadim[-1]]
            self.dnnact=[tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.tanh,tf.nn.relu]

        self.lstmlayer=[]
        self.cnnlayer=[]
        self.cnnact=[]
