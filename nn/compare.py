import pandas as pd
import numpy as np

dfdir='../../data/nn/tensorflow/CNNmodelpred2/dataframe/'

for scani in range(1,7):
    df=pd.read_csv(dfdir+'valpredscan'+str(scani)+'row1.csv')
    df['residual']=df['truth']-df['valpred']
    residualmean=df.groupby('truth').mean()
    arrayresimean=np.array(residualmean['residual'])
    arrayresistd=np.array(df.groupby('truth').std()['residual'])
    arraytrueposition=np.array(residualmean.index)
    arraymeasureposition=np.array(residualmean['valpred'])

    df=pd.read_csv(dfdir+'valpredscan'+str(scani)+'row2.csv')
    df['residual']=df['truth']-df['valpred']
    residualmean=df.groupby('truth').mean()
    arrayresimean=np.concatenate((arrayresimean,np.array(residualmean['residual'])),axis=0)
    arrayresistd=np.concatenate((arrayresistd,np.array(df.groupby('truth').std()['residual'])),axis=0)
    arraytrueposition=np.concatenate((arraytrueposition,np.array(residualmean.index)+3.5),axis=0)
    arraymeasureposition=np.concatenate((arraymeasureposition,np.array(residualmean['valpred'])+3.5),axis=0)
    
    outdf = pd.DataFrame({'measurepos':arraymeasureposition,'truepos':arraytrueposition,'residualmean':arrayresimean,'residualstd':arrayresistd})
    # outdf.to_csv(dfdir+'afterNN'+str(scani)+'.csv')

