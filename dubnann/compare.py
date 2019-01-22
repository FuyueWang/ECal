import pandas as pd


dfdir='../../data/dubnann/tensorflow/CNNmodelpred/dataframe/'

for scani in range(1):
    df=pd.read_csv(dfdir+'valpredscan'+str(scani)+'.csv')
    df['residual']=df['truth']-df['valpred']
    residualmean=df.groupby('truth').mean()
    arraymean=np.array(residualmean)
    arrayposition=
