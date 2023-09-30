import pandas as pd
from datetime import datetime

def clean_data(df, questionTitles):
    dates = ['startJourney', 'endJourney','reviewDate']
    for d in dates:
        df[d] = pd.to_datetime(df[d].apply(lambda x : datetime.fromtimestamp(int(x)/1000)))
    df['ratingSummary'] = df['ratingSummary'].astype('float32')
    df['comments'] = df['comments'].apply(lambda x: x[0]['value'])
    df['lengthOfStay'] = df['endJourney'] - df['startJourney']
    try :
        df.rename(columns={'Saat nginep di sini, apa jenis perjalananmu?':'tripType'}, inplace=True)
        df['tripType'].fillna('Tidak Jawab', inplace=True)
    except:
        print("Data does not complete : tripType Missing!")
    df.dropna(axis=1, how='all', inplace=True)

    return df.drop_duplicates('submitId').drop(columns='submitId'), [x for x in df.columns if 'Rating_' in x]
    # df.drop(columns=['comments'], inplace=True)

def filter_df(df,rating,trips, date_start, date_end, stay):
    # print(rating, trips, date_start, date_end)
    p = df[
        (df['ratingSummary'] <= rating[1]) & (df['ratingSummary']>=rating[0])&
        (df['reviewDate'].dt.date <= date_end) & (df['reviewDate'].dt.date>=date_start)&
        (df['tripType'].apply(lambda x: x in trips)) &
        (df['lengthOfStay'].dt.days >= stay[0]) & (df['lengthOfStay'].dt.days <= stay[1])
    ]
    return p
   