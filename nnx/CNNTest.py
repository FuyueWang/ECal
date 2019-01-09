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

trainsize=400000
testsize=22900 


learningi=tf.placeholder("float",[1])
learning_rate=0.01*pow(0.1,learningi[0])

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
# conv3 = tf.layers.conv2d(conv2, 128, 2, activation=tf.nn.relu)
conv4 = tf.layers.conv2d(conv2, 32, 2, activation=tf.nn.relu)
# # conv3 = tf.layers.max_pooling2d(conv2, 2, 2)

fc1 = tf.contrib.layers.flatten(conv4)

outputs = tf.contrib.layers.fully_connected(fc1,30,activation_fn=tf.nn.tanh )
outputs = tf.contrib.layers.dropout(fc1, keep_prob=0.9)


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

realtestsize=datafromfile.shape[0]-trainsize-testsize
fig = plt.figure(figsize=(9,7))


with tf.Session() as sess:
    sess.run(init)

    new_saver = tf.train.import_meta_graph(ModelDir+'test-100.meta')
    new_saver.restore(sess, tf.train.latest_checkpoint(ModelDir))
    thislearning=[4]
    teststd=1
    while teststd>0.55:
        testinputx = datafromfile[trainsize+testsize:,:-1].reshape(realtestsize,datasizex,datasizey,datachannel)
        testinputy=datafromfile[trainsize+testsize:,-1].reshape(realtestsize,1)
        teststd,testlos,testposresidual,testpred=sess.run([posstd,loss,mean,prediction],feed_dict={x:testinputx, y: testinputy, learningi: thislearning})
        print("For iter",iter,"test: pos resolution", teststd[0],"cm, Loss",testlos ,"residual",testposresidual,"cm")
    testpredlist=[testpred[k][0] for k in range(testpred.shape[0])]
    testtruthlist=[testinputy[k][0] for k in range(testinputy.shape[0])]
    df = pd.DataFrame(data={'testpred':testpredlist, 'truth':testtruthlist})
    df.to_csv(ModelDir+'testpred.csv')
    fig = plt.figure(figsize=(5,4))
    ax = plt.subplot2grid((1,1), (0,0))
    ax.hist(testpred-testinputy,bins=np.linspace(-2, 2,70),label='test',color='r',histtype='step')
    plt.show()
