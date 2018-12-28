import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle
import warnings
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 

warnings.filterwarnings("ignore")

outdatadir='../../data/nn/tensorflow/'
createmap=True

trainsize=40000
batchsize=5000 #5000
testsize=2200 #99000

stepNbofiter=4000

learningi=tf.placeholder("float",[1])
learning_rate=0.05*pow(0.1,learningi[0])

datasizex=9
datasizey=9
datachannel=3
outputdim=1
inputdim=243
#input image placeholder
x=tf.placeholder("float",[None,datasizex,datasizey,datachannel])
y=tf.placeholder("float",[None,outputdim])

conv1 = tf.layers.conv2d(x, 32, 2, activation=tf.nn.tanh)
# conv1 = tf.layers.max_pooling2d(conv1, 2, 1)

conv2 = tf.layers.conv2d(conv1, 64, 2, activation=tf.nn.tanh)
# # conv2 = tf.layers.max_pooling2d(conv2, 2, 1)
conv3 = tf.layers.conv2d(conv2, 128, 2, activation=tf.nn.relu)
conv4 = tf.layers.conv2d(conv3, 32, 2, activation=tf.nn.relu)
# # conv3 = tf.layers.max_pooling2d(conv2, 2, 2)

fc1 = tf.contrib.layers.flatten(conv4)

# outputs = tf.contrib.layers.fully_connected(fc1,100,activation_fn=tf.nn.tanh )
outputs = tf.contrib.layers.dropout(fc1, keep_prob=0.85)


prediction = tf.contrib.layers.fully_connected(outputs,1) #,weights_regularizer= tf.contrib.layers.l2_regularizer(0.2))

loss = tf.losses.mean_squared_error(y,prediction)
opt=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

correct_prediction=prediction-y
mean, var = tf.nn.moments(correct_prediction, axes=[0])
posstd=tf.sqrt(var) #cm

saver = tf.train.Saver(max_to_keep=4000)
#initialize variables
init=tf.global_variables_initializer()

scani=1
ModelDir=outdatadir+'CNNmodels'+str(scani)+'/'
with open(outdatadir+'cnnwavescan'+str(scani)+'.dat', 'rb') as f:
    datafromfile = pickle.load(f)

np.random.shuffle(datafromfile)


fig = plt.figure(figsize=(9,7))
Nbofbatch=trainsize//batchsize
if createmap:
    Nboflearn=1;
for learni in range(0,Nboflearn):
    thislearning=[learni]
    if createmap:
        Nbofiter=210
        PrintCount=100
        ModelSaverCount=100
    else:
        Nbofiter=stepNbofiter*(1+learni*2)+10
        PrintCount=100
        ModelSaverCount=Nbofiter-10

    
    with tf.Session() as sess:
        sess.run(init)
        iter=0
        if createmap == False:
            new_saver = tf.train.import_meta_graph(ModelDir+'test-100.meta')
            new_saver.restore(sess, tf.train.latest_checkpoint(ModelDir))
        
     
        trainloss=[]
        trainreso=[]
        testloss=[]
        testreso=[]        
        while iter<Nbofiter:
            startbatch=iter%Nbofbatch
            
            inputx=datafromfile[startbatch*batchsize:(startbatch+1)*batchsize,:-1].reshape(batchsize,datasizex,datasizey,datachannel)
            inputy=datafromfile[startbatch*batchsize:(startbatch+1)*batchsize,-1].reshape(batchsize,1)

            sess.run(opt, feed_dict={x: inputx, y: inputy, learningi: thislearning})
            if iter % PrintCount==0:
                std,los,posresidual,trainpred=sess.run([posstd,loss,mean,prediction],feed_dict={x:inputx, y: inputy, learningi: thislearning})
                trainloss.append(los)
                trainreso.append(std[0])
                
                testinputx = datafromfile[trainsize:trainsize+testsize,:-1].reshape(testsize,datasizex,datasizey,datachannel)
                testinputy=datafromfile[trainsize:trainsize+testsize,-1].reshape(testsize,1)
                teststd,testlos,testposresidual,testpred=sess.run([posstd,loss,mean,prediction],feed_dict={x:testinputx, y: testinputy, learningi: thislearning})
                testloss.append(testlos)
                testreso.append(teststd[0])

                ax = plt.subplot2grid((2,2), (0,0))
                ax.hist(trainpred-inputy,bins=np.linspace(-2, 2,70),label='train',color='k',histtype='step')
                ax.hist(testpred-testinputy,bins=np.linspace(-2, 2,70),label='test',color='r',histtype='step')
                plt.title('residual')
                ax = plt.subplot2grid((2,2), (0,1))
                ax.hist(inputy,bins=np.linspace(7, 14,70),label='truth',color='k',histtype='step')
                ax.hist(trainpred,bins=np.linspace(7, 14,70),label='pred',color='r',histtype='step')
                plt.title('position')
                ax = plt.subplot2grid((2,2), (1,0))
                ax.plot(trainloss,label='train',color='k')
                ax.plot(testloss,label='test',color='r')
                plt.title('loss')
                ax = plt.subplot2grid((2,2), (1,1))
                ax.plot(trainreso,label='train',color='k')
                ax.plot(testreso,label='test',color='r')
                plt.title('loss')
                plt.draw()
                plt.pause(0.001)
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
        
