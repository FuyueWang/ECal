import matplotlib
import matplotlib.pyplot as plt 
import numpy as np


def plotclasstrain(fig1,fig2,fig3,fig4,figname='donotsave'):
    """
    fig1: [fp,tp] plt.plot
    fig2: [traintruth,trainpred] plt.hist 
    fig3: [trainloss,validateloss] plt.plot
    fig4: [trainresult,validateresult] plt.plot
    """

    ax = plt.subplot2grid((2,2), (0,0))
                    
    # ax.hist(trainpred-inputy,bins=np.linspace(-1,1,50),label='train',color='k',histtype='step')
    # ax.hist(valpred-valy,bins=np.linspace(-1.,1,50),label='validation',color='r',histtype='step')
    ax.plot(fig1[0],fig1[1],color='k')
    plt.title('ROC')
    plt.xlabel('False Positive')
    plt.ylabel('True Positive')
    
    ax = plt.subplot2grid((2,2), (0,1))
    ax.hist(fig2[0],bins=np.linspace(-1.5,3.5,30),label='truth',color='k',histtype='step')
    ax.hist(fig2[1],bins=np.linspace(-1.5,3.5,30),label='prediction',color='r',histtype='step')
    plt.title('label')
    plt.legend(loc='upper right')

    ax = plt.subplot2grid((2,2), (1,0))
    ax.plot(fig3[0],label='train',color='k')
    ax.plot(fig3[1],label='validation',color='r')
    plt.title('loss')
    plt.legend(loc='upper right')

    ax = plt.subplot2grid((2,2), (1,1))
    ax.plot(fig4[0],label='train',color='k')
    ax.plot(fig4[1],label='validation',color='r')
    plt.title('Accurarcy')
    plt.legend(loc='upper left')

    if figname is not 'donotsave':
        plt.savefig(figname) #,dpi=200)
    plt.draw()
    plt.pause(0.001)
    
def plotclassval(fig1,fig2,fig3,fig4,figname='donotsave'):
    """
    fig1: [fp,tp] plt.plot
    fig2: [valtruth,valpred] plt.hist 
    """

    ax = plt.subplot2grid((2,2), (0,0))
                    
    # ax.hist(trainpred-inputy,bins=np.linspace(-1,1,50),label='train',color='k',histtype='step')
    # ax.hist(valpred-valy,bins=np.linspace(-1.,1,50),label='validation',color='r',histtype='step')
    ax.plot(fig1[0],fig1[1],color='k')
    plt.title('ROC')
    plt.xlabel('False Positive')
    plt.ylabel('True Positive')
    
    ax = plt.subplot2grid((2,2), (0,1))
    ax.hist(fig2[0],bins=np.linspace(-1.5,3.5,30),label='truth',color='k',histtype='step')
    ax.hist(fig2[1],bins=np.linspace(-1.5,3.5,30),label='prediction',color='r',histtype='step')
    plt.title('label')
    plt.legend(loc='upper right')

    if figname is not 'donotsave':
        plt.savefig(figname) #,dpi=200)
    plt.draw()
    plt.pause(0.001)

    
def plotregtrain(fig1,fig2,fig3,fig4,figname='donotsave'):
    ax = plt.subplot2grid((2,2), (0,0))
    ax.hist(fig1[0],bins=np.linspace(-2, 2,70),label='train',color='k',histtype='step')
    ax.hist(fig1[1],bins=np.linspace(-2, 2,70),label='test',color='r',histtype='step')
    plt.title('residual')
    plt.legend(loc='upper right')
    ax = plt.subplot2grid((2,2), (0,1))
    ax.hist(fig2[0],bins=np.linspace(0, 5,70),label='truth',color='k',histtype='step')
    ax.hist(fig2[1],bins=np.linspace(0, 5,70),label='pred',color='r',histtype='step')
    plt.title('position')
    plt.legend(loc='upper right')
    ax = plt.subplot2grid((2,2), (1,0))
    ax.plot(fig3[0],label='train',color='k')
    ax.plot(fig3[1],label='test',color='r')
    plt.title('loss')
    plt.legend(loc='upper right')
    ax = plt.subplot2grid((2,2), (1,1))
    ax.plot(fig4[0],label='train',color='k')
    ax.plot(fig4[1],label='test',color='r')
    plt.title('resolution')
    plt.legend(loc='upper right')
    if figname is not 'donotsave':
        plt.savefig(figname) #,dpi=200)
    plt.draw()
    plt.pause(0.001)

def plotregval(fig1,fig2,figname='donotsave'):
    ax = plt.subplot2grid((1,2), (0,0))
    ax.hist(fig1,bins=np.linspace(-2, 2,70),label='validate',color='k',histtype='step')
    plt.title('residual')
    ax = plt.subplot2grid((1,2), (0,1))
    ax.hist(fig2[0],bins=np.linspace(9.7, 14,70),label='truth',color='k',histtype='step')
    ax.hist(fig2[1],bins=np.linspace(9.7, 14,70),label='pred',color='r',histtype='step')
    plt.title('position')
    plt.legend(loc='upper right')
    if figname is not 'donotsave':
        plt.savefig(figname) #,dpi=200)
    plt.draw()
    plt.pause(0.001)
