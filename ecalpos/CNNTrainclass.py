import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle
import warnings
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt 
from calibratedata import ReadTrainData
warnings.filterwarnings("ignore")
outdatadir="../../data/ecalpos/"
outtxtdir="../../txt/ecalpos/"
createmap=False

trainsize=500000
batchsize=10000 #5000
testsize=20000 #99000
if createmap:
    Nbofiter=210000
    PrintCount=100
    ModelSaverCount=100
else:
    Nbofiter=400010
    PrintCount=100
    ModelSaverCount=80000


learningi=tf.placeholder("float",[1])
learning_rate=0.05*pow(0.1,learningi[0])

datasizex=3
datasizey=3
datachannel=1
outputdim=7
inputdim=9
#input image placeholder
x=tf.placeholder("float",[None,datasizex,datasizey,datachannel])
y=tf.placeholder("float",[None,outputdim])

conv1 = tf.layers.conv2d(x, 32, 1, activation=tf.nn.relu)
# conv1 = tf.layers.max_pooling2d(conv1, 2, 1)

conv2 = tf.layers.conv2d(conv1, 64, 1, activation=tf.nn.relu)
# # conv2 = tf.layers.max_pooling2d(conv2, 2, 1)
conv3 = tf.layers.conv2d(conv2, 64, 1, activation=tf.nn.relu)
conv4 = tf.layers.conv2d(conv3, 128, 2, activation=tf.nn.relu)
# # conv3 = tf.layers.max_pooling2d(conv2, 2, 2)

fc1 = tf.contrib.layers.flatten(conv4)
prediction = tf.contrib.layers.fully_connected(fc1,outputdim) 

# outputs = tf.contrib.layers.fully_connected(fc1,100,activation_fn=tf.nn.tanh )

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
opt=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
correct_prediction=tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

saver = tf.train.Saver(max_to_keep=4000)
#initialize variables
init=tf.global_variables_initializer()

ModelDir=outdatadir+"CNNClassmodels/"

Intdf=ReadClassTrainData() #pd.read_csv(outdatadir+'dfdata/'+'scanfrom'+str(scanID[scanid])+'Intdf.csv')
# Intdf=Intdf[Intdf['standPosy']<1.4][Intdf['standPosy']>-1.4]

# Intdf.shape
Nbofbatch=trainsize//batchsize
for learni in range(1,4):
    thislearning=[learni]
    with tf.Session() as sess:
        sess.run(init)
        iter=1
        if createmap == False:
            new_saver = tf.train.import_meta_graph(ModelDir+'test-100.meta')
            new_saver.restore(sess, tf.train.latest_checkpoint(ModelDir))
        
     
        trainloss=[]
        trainreso=[]
        testloss=[]
        testreso=[]        
        while iter<Nbofiter:
            startbatch=iter%Nbofbatch
            dim0=list(Intdf['ch0'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim1=list(Intdf['ch1'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim2=list(Intdf['ch2'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim3=list(Intdf['ch3'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim4=list(Intdf['ch4'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim5=list(Intdf['ch5'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim6=list(Intdf['ch6'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim7=list(Intdf['ch7'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim8=list(Intdf['ch8'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])

            inputx=np.array(dim0+dim1+dim2+dim3+dim4+dim5+dim6+dim7+dim8).reshape(inputdim,batchsize).T.reshape(batchsize,datasizex,datasizey,datachannel)
            inputy=np.array(Intdf['standPosy'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]).reshape(batchsize,1)

            sess.run(opt, feed_dict={x: inputx, y: inputy, learningi: thislearning})
            if iter % PrintCount==0:
                std,los,posresidual=sess.run([posstd,loss,mean],feed_dict={x:inputx, y: inputy, learningi: thislearning})
                trainloss.append(los)
                trainreso.append(std[0])
                testdim0=list(Intdf['ch0'].iloc[trainsize:trainsize+testsize])
                testdim1=list(Intdf['ch1'].iloc[trainsize:trainsize+testsize])
                testdim2=list(Intdf['ch2'].iloc[trainsize:trainsize+testsize])
                testdim3=list(Intdf['ch3'].iloc[trainsize:trainsize+testsize])
                testdim4=list(Intdf['ch4'].iloc[trainsize:trainsize+testsize])
                testdim5=list(Intdf['ch5'].iloc[trainsize:trainsize+testsize])
                testdim6=list(Intdf['ch6'].iloc[trainsize:trainsize+testsize])
                testdim7=list(Intdf['ch7'].iloc[trainsize:trainsize+testsize])
                testdim8=list(Intdf['ch8'].iloc[trainsize:trainsize+testsize])

                testinputx = np.array(testdim0+testdim1+testdim2+testdim3+testdim4+testdim5+testdim6+testdim7+testdim8).reshape(inputdim,testsize).T.reshape(testsize,datasizex,datasizey,datachannel)
                testinputy=np.array(Intdf['standPosy'].iloc[trainsize:trainsize+testsize]).reshape(testsize,1)
                teststd,testlos,testposresidual=sess.run([posstd,loss,mean],feed_dict={x:testinputx, y: testinputy, learningi: thislearning})
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
        
