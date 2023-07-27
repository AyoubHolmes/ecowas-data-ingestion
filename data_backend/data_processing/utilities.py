import pandas as pd


def add_timestamp(df):
    df['date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
    return df

