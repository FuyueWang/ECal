import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle
import warnings
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt 
from readrawdata import ReadMaxData
from readrawdata import ReadIntData

warnings.filterwarnings("ignore")
outdatadir="../../data/ecalpos/"
outtxtdir="../../txt/ecalpos/"
createmap=False

trainsize=210000 
batchsize=70000 #5000
testsize=60000 #99000
if createmap:
    Nbofiter=2010
    PrintCount=10
    ModelSaverCount=10
else:
    Nbofiter=8010
    PrintCount=100
    ModelSaverCount=4000

learningi=tf.placeholder("float",[1])
learning_rate=0.001*pow(0.1,learningi[0])

inputdim=3
outputdim=1


#input image placeholder
x=tf.placeholder("float",[None,inputdim])
#input label placeholder
y=tf.placeholder("float",[None,outputdim])
# plabel=tf.placeholder("float",[test_size])

outputs = tf.contrib.layers.fully_connected(x,16,activation_fn=tf.nn.tanh)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,14 ,activation_fn=tf.nn.tanh)
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,16,activation_fn=tf.nn.tanh )
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,17,activation_fn=tf.nn.tanh )
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,18 ,activation_fn=tf.nn.tanh)
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,16,activation_fn=tf.nn.tanh )
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,13,activation_fn=tf.nn.tanh )
outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
prediction = tf.contrib.layers.fully_connected(outputs,1) #,weights_regularizer= tf.contrib.layers.l2_regularizer(0.2))

loss = tf.losses.mean_squared_error(y,prediction)
opt=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

correct_prediction=prediction-y
mean, var = tf.nn.moments(correct_prediction, axes=[0])
posstd=tf.sqrt(var) #cm

saver = tf.train.Saver(max_to_keep=4000)
#initialize variables
init=tf.global_variables_initializer()

ModelDir=outdatadir+"DNNmodels/"

Intdf=ReadIntData(outdatadir+'dfdata/',2,2) #pd.read_csv(outdatadir+'dfdata/'+'scanfrom'+str(scanID[scanid])+'Intdf.csv')
Intdf=Intdf.sample(frac=1)

# Intdf.shape
Nbofbatch=trainsize//batchsize
for learni in range(1,4):
    thislearning=[learni]
    with tf.Session() as sess:
        sess.run(init)
        iter=1
        if createmap == False:
            new_saver = tf.train.import_meta_graph(ModelDir+'test-180.meta')
            new_saver.restore(sess, tf.train.latest_checkpoint(ModelDir))

        trainloss=[]
        trainreso=[]
        testloss=[]
        testreso=[]
        train0=[]
        train1=[]
        train2=[]
        posylist=[]
        
        while iter<Nbofiter:
            startbatch=iter%Nbofbatch
            dim0=list(Intdf['IntCh0'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]+Intdf['IntCh1'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]+Intdf['IntCh2'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]) 
            dim1=list(Intdf['IntCh3'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]+Intdf['IntCh4'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]+Intdf['IntCh5'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]) 
            dim2=list(Intdf['IntCh6'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]+Intdf['IntCh7'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]+Intdf['IntCh8'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim3=list(Intdf['estimatepos'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            inputx=np.array(dim0+dim1+dim2).reshape(inputdim,batchsize).T
            inputy=np.array(Intdf['Posy'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]).reshape(batchsize,1)

            sess.run(opt, feed_dict={x: inputx, y: inputy, learningi: thislearning})

        
            
            if iter % PrintCount==0:
                std,los,posresidual=sess.run([posstd,loss,mean],feed_dict={x:inputx, y: inputy, learningi: thislearning})
                trainloss.append(los)
                trainreso.append(std[0])

                testdim0=list(Intdf['IntCh0'].iloc[trainsize:trainsize+testsize]+Intdf['IntCh1'].iloc[trainsize:trainsize+testsize]+Intdf['IntCh2'].iloc[trainsize:trainsize+testsize]) 
                testdim1=list(Intdf['IntCh3'].iloc[trainsize:trainsize+testsize]+Intdf['IntCh4'].iloc[trainsize:trainsize+testsize]+Intdf['IntCh5'].iloc[trainsize:trainsize+testsize]) 
                testdim2=list(Intdf['IntCh6'].iloc[trainsize:trainsize+testsize]+Intdf['IntCh7'].iloc[trainsize:trainsize+testsize]+Intdf['IntCh8'].iloc[trainsize:trainsize+testsize])
                testdim3=list(Intdf['estimatepos'].iloc[trainsize:trainsize+testsize])
                testinputx = np.array(testdim0+testdim1+testdim2).reshape(inputdim,testsize).T
                testinputy=np.array(Intdf['Posy'].iloc[trainsize:trainsize+testsize]).reshape(testsize,1)
                teststd,testlos,testposresidual=sess.run([posstd,loss,mean],feed_dict={x:testinputx, y: testinputy, learningi: thislearning})

                df1= pd.DataFrame(data={'dim0':testdim0, 'dim1':testdim1, 'dim2':testdim2,'posy':list(testinputy)})
           
                testloss.append(testlos)
                testreso.append(teststd[0])
                print("learning rate",sess.run(learning_rate,feed_dict={x:inputx, y: inputy, learningi: thislearning}))
                print("For iter",iter,"train: pos resolution", std[0],"cm, Loss",los ,"residual",posresidual,"cm")
                print("For iter",iter,"test: pos resolution", teststd[0],"cm, Loss",testlos ,"residual",testposresidual,"cm")
            if iter % ModelSaverCount ==0:
                if createmap:
                    saver.save(sess, ModelDir+"test",global_step=iter,write_meta_graph=True)
                else:
                    saver.save(sess, ModelDir+"test",global_step=iter,write_meta_graph=False)
                df = pd.DataFrame(data={'train_loss':trainloss, 'test_loss':testloss, 'train_reso':trainreso,'test_reso':testreso})
                df.to_csv(ModelDir+"Nb"+str(iter//ModelSaverCount)+"_"+str(iter)+'.csv')
            iter=iter+1
        
