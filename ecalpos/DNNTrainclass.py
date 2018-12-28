import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle
import warnings
import pandas as pd
import matplotlib.pyplot as plt 
from readrawdata import ReadMaxData
from readrawdata import ReadIntData
from calibratedata import ReadTrainData
from calibratedata import ReadClassTrainData
warnings.filterwarnings("ignore")
outdatadir="../../data/ecalpos/"
outtxtdir="../../txt/ecalpos/"
createmap=False

trainsize=50000
batchsize=10000 #5000
testsize=20000 #99000
if createmap:
    Nbofiter=210
    PrintCount=100
    ModelSaverCount=100
else:
    Nbofiter=400010
    PrintCount=500
    ModelSaverCount=80000

learningi=tf.placeholder("float",[1])
learning_rate=0.01*pow(0.1,learningi[0])

inputdim=9
outputdim=7

#input image placeholder
x=tf.placeholder("float",[None,inputdim])
#input label placeholder
y=tf.placeholder("float",[None,outputdim])
# plabel=tf.placeholder("float",[test_size])

outputs = tf.contrib.layers.fully_connected(x,16,activation_fn=tf.nn.sigmoid)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,15 ,activation_fn=tf.nn.sigmoid)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,16 ,activation_fn=tf.nn.sigmoid)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,17 ,activation_fn=tf.nn.sigmoid)
# outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)

outputs = tf.contrib.layers.fully_connected(outputs,32,activation_fn=tf.nn.sigmoid )
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,14,activation_fn=tf.nn.sigmoid )
# # outputs = tf.contrib.layers.dropout(outputs, keep_prob=0.85)
outputs = tf.contrib.layers.fully_connected(outputs,16,activation_fn=tf.nn.sigmoid )
prediction = tf.contrib.layers.fully_connected(outputs,outputdim) #,weights_regularizer= tf.contrib.layers.l2_regularizer(0.2))


loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
opt=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
correct_prediction=tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

saver = tf.train.Saver(max_to_keep=4000)
#initialize variables
init=tf.global_variables_initializer()

ModelDir=outdatadir+"DNNClassmodels/"

readtraindf=ReadClassTrainData()
traindf=readtraindf

# traindf=(readtraindf-readtraindf.mean())/readtraindf.std()[['ch'+str(k) for k in range(9)]]
# traindf['standPosy']=readtraindf['standPosy']
# traindf=readtraindf
# data=np.random.random_sample((70000,9))
# traindf=pd.DataFrame(data=data,columns=['ch'+str(k) for k in range(9)])
# traindf['standPosy']=traindf['ch0']+traindf['ch1']+traindf['ch2']+traindf['ch3']+traindf['ch4']+traindf['ch5']+traindf['ch6']+traindf['ch7']+traindf['ch8']

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
            dim0=list(traindf['ch0'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim1=list(traindf['ch1'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim2=list(traindf['ch2'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim3=list(traindf['ch3'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim4=list(traindf['ch4'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim5=list(traindf['ch5'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim6=list(traindf['ch6'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim7=list(traindf['ch7'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            dim8=list(traindf['ch8'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            # dim9=list(traindf['estimatepos'].iloc[startbatch*batchsize:(startbatch+1)*batchsize])
            inputx=np.array(dim0+dim1+dim2+dim3+dim4+dim5+dim6+dim7+dim8).reshape(inputdim,batchsize).T
            # inputx=np.array(dim9).reshape(inputdim,batchsize).T
            

            
            inputy=np.array(list(traindf['label'].iloc[startbatch*batchsize:(startbatch+1)*batchsize]))

            sess.run(opt, feed_dict={x: inputx, y: inputy, learningi: thislearning})
            if iter % PrintCount==0:
                trainaccuracy,los=sess.run([accuracy,loss],feed_dict={x:inputx, y: inputy, learningi: thislearning})
                trainloss.append(los)
                trainreso.append(trainaccuracy)
                testdim0=list(traindf['ch0'].iloc[trainsize:trainsize+testsize])
                testdim1=list(traindf['ch1'].iloc[trainsize:trainsize+testsize])
                testdim2=list(traindf['ch2'].iloc[trainsize:trainsize+testsize])
                testdim3=list(traindf['ch3'].iloc[trainsize:trainsize+testsize])
                testdim4=list(traindf['ch4'].iloc[trainsize:trainsize+testsize])
                testdim5=list(traindf['ch5'].iloc[trainsize:trainsize+testsize])
                testdim6=list(traindf['ch6'].iloc[trainsize:trainsize+testsize])
                testdim7=list(traindf['ch7'].iloc[trainsize:trainsize+testsize])
                testdim8=list(traindf['ch8'].iloc[trainsize:trainsize+testsize])
                # testdim9=list(traindf['estimatepos'].iloc[trainsize:trainsize+testsize])
                testinputx = np.array(testdim0+testdim1+testdim2+testdim3+testdim4+testdim5+testdim6+testdim7+testdim8).reshape(inputdim,testsize).T
                # testinputx = np.array(testdim9).reshape(inputdim,testsize).T
                testinputy=np.array(list(traindf['label'].iloc[trainsize:trainsize+testsize]))
                testacc,testlos=sess.run([accuracy,loss],feed_dict={x:testinputx, y: testinputy, learningi: thislearning})
                testloss.append(testlos)
                testreso.append(testacc)
                # plt.hist(testpred)
                # plt.show()
                # np.savetxt('testpred.txt',testpred)
                # np.savetxt('testdim9.txt',np.array(testdim9))
                # np.savetxt('Posy.txt',testinputy)
                # testpre=np.loadtxt('testpred.txt')
                # truth=np.loadtxt('Posy.txt')
                print("learning rate",sess.run(learning_rate,feed_dict={x:inputx, y: inputy, learningi: thislearning}))
                print("For iter",iter,"train: acc", trainaccuracy,", Loss",los)
                print("For iter",iter,"test: acc", testacc,", Loss",testlos)
            if iter % ModelSaverCount ==0:
                if createmap:
                    saver.save(sess, ModelDir+"test",global_step=iter,write_meta_graph=True)
                else:
                    saver.save(sess, ModelDir+"test",global_step=iter,write_meta_graph=False)
                df = pd.DataFrame(data={'train_loss':trainloss, 'test_loss':testloss, 'train_reso':trainreso,'test_reso':testreso})
                df.to_csv(ModelDir+"Nb"+str(iter//ModelSaverCount)+"_"+str(iter)+'.csv')
            iter=iter+1
        
