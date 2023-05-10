import pandas as pd
def preprocess(df):
    df=df.drop('Serial Number',axis=1)
    df=df.fillna('Missing Values')
    #df=df.set_index('Country')
    return df
def preprocess1(df):
    df.Date_reported=pd.to_datetime(df.Date_reported)
    df['Year']=df.Date_reported.dt.year
    df['Month']=df.Date_reported.dt.month_name()
    return df


