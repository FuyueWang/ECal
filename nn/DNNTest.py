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

outputdim=1
inputdim=9

#input image placeholder
x=tf.placeholder("float",[None,inputdim])
#input label placeholder
y=tf.placeholder("float",[None,outputdim])
# plabel=tf.placeholder("float",[test_size])

outputs = tf.contrib.layers.fully_connected(x,16,activation_fn=tf.nn.tanh)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,25 ,activation_fn=tf.nn.tanh)
outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,16 ,activation_fn=tf.nn.tanh)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,19 ,activation_fn=tf.nn.tanh)
outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

# outputs = tf.contrib.layers.fully_connected(outputs,12,activation_fn=tf.nn.relu )
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
# outputs = tf.contrib.layers.fully_connected(outputs,7,activation_fn=tf.nn.relu )
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,8,activation_fn=tf.nn.tanh )
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
ModelDir=outdatadir+"DNNmodels"+str(scani)+'/'

with open(outdatadir+'integralscan'+str(scani)+'.dat', 'rb') as f:
    datafromfile = pickle.load(f)
    
realtestsize=datafromfile.shape[0]-trainsize-testsize
fig = plt.figure(figsize=(9,7))


with tf.Session() as sess:
    sess.run(init)

    new_saver = tf.train.import_meta_graph(ModelDir+'test-100.meta')
    new_saver.restore(sess, tf.train.latest_checkpoint(ModelDir))
    thislearning=[4]
    teststd=1
    while teststd>0.5307:
        testinputx = datafromfile[trainsize+testsize:,:-1].reshape(realtestsize,inputdim)
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
