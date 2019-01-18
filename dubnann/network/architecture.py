import tensorflow as tf
from tensorflow.contrib import rnn
class architecture():
    """
    define the architecture of the newtork
    This class contains several single cnn,dnn and lstm networks, and you can arrange them together in a way you need

    private fcn:
    cnnetwork()
    dnnnetwork()
    lstmnetwork()

    public fcn:
    network(): a combo of the 3 private fcn
    """
    
    def __init__(self, cnn=dict(layer=[],activation=[]), lstm=dict(layer=[]), dnn=dict(layer=[],activation=[])):
        self.cnnarch=cnn
        self.lstmarch=lstm
        self.dnnarch=dnn 
    
    def cnnnetwork(self,conv,architecture=dict(layer=[32,64,32],activation=[tf.nn.tanh,tf.nn.tanh,tf.nn.relu])):
        for k in range(len(architecture['layer'])-1):
            conv = tf.layers.conv2d(conv, architecture['layer'][k], 2, activation=architecture['activation'][k])
        conv = tf.contrib.layers.flatten(conv)
        return conv

    def dnnnetwork(self,fc,architecture=dict(layer=[10,1],activation=[tf.nn.relu,None])):
        for k in range(len(architecture['layer'])-1):
            fc = tf.contrib.layers.dropout(fc, keep_prob=0.9)
            fc = tf.contrib.layers.fully_connected(fc,architecture['layer'][k],activation_fn=architecture['activation'][k] )
        fc = tf.contrib.layers.dropout(fc, keep_prob=0.9)
        fc = tf.contrib.layers.fully_connected(fc,architecture['layer'][-1])
        return fc


    def lstmnetwork(self,lstm,architecture=dict(layer=[10,1])):
        lstm=tf.unstack(lstm ,lstm.shape[1],1)
        input=lstm
        for k in range(len(architecture['layer'])):
            lstm=rnn.DropoutWrapper(rnn.BasicLSTMCell(architecture['layer'][k],forget_bias=1), input_keep_prob=0.95, output_keep_prob=0.95, state_keep_prob=0.95)
        lstm,_=rnn.static_rnn(lstm,input,dtype="float32")
        return lstm[-1]

    
    def network(self,x):
        """
        define your own specific network here
        """
        if len(self.cnnarch['layer'])==0: # without cnn
            if len(self.lstmarch['layer'])==0: # without lstm
                if len(self.dnnarch['layer'])==0: # without dnn
                    print("Vacant Netowrk")
                else: # only dnn
                    y=self.dnnnetwork(x,self.dnnarch)
            else:  # lstm network
                if len(self.dnnarch['layer'])==0: # without dnn
                    y=self.lstmnetwork(x,self.lstmarch)
                else: # with dnn
                    y=self.dnnnetwork(self.lstmnetwork(x,self.lstmarch),self.dnnarch)
        else: # cnn network
            if len(self.dnnarch['layer'])==0: # without dnn
                y=self.cnnnetwork(x,self.cnnarch)
            else: # with dnn
                y=self.dnnnetwork(self.cnnnetwork(x,self.cnnarch),self.dnnarch)
        return y
