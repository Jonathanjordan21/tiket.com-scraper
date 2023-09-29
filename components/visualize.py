from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.dates as mdates

def wordcloud(df_data, stop_words):
    nltk.download('stopwords')
    stop = stopwords.words('indonesian')
 
    strs = ' '.join(
        df_data.comments.values
    ).lower()

    pattern = r'\b[a-zA-Z]{5,}\b'
    tokens = nltk.regexp_tokenize(strs, f'{pattern}(?!-nya\\b)')
    # print(tokens)
    stop = stop+['overall', 'untuk', 'hotel','villa', 'kamar', 'karna', 'karena', 'menginap', 'inap']+stop_words

    strs = " ".join([token for token in tokens if token not in stop])
    fig, ax = plt.subplots(figsize=(12,12))
    try :
        ax.imshow(WordCloud().generate(strs))
    except:
        print("Error Occur! WordCloud need at least one Word")
        pass

    ax.axis('off')

    return fig, ax



def pie_chart(df):

    h = df.groupby(['tripType']).count()['ratingSummary'].sort_values()
    fig, ax = plt.subplots(figsize=(12,12))

    explode = [0]*len(h.index)
    explode[0] = 0.5

    return fig, ax.pie(
        h, 
        # autopct='%1.2f%%',
        labels=h.index,
        shadow = True,
        explode=explode,
        autopct = lambda p : f'{round(p*sum(h)/100)}',
        colors = sns.color_palette("Blues"),
        wedgeprops={'linewidth':5.0, 'edgecolor':'white'},
        textprops={'fontsize':21}
    )

def customer_count(df_data, year):
    # print(year)
    df_data = df_data.sort_values('reviewDate')
    df_data['month']=df_data.reviewDate.dt.month
    print(df_data['month'].unique())
    fig, ax = plt.subplots(figsize=(12,12))
    # print(df_data['month'].unique())
    unit = ['dec','jan','feb','mar','apr','may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    val = {i:u for i,u in enumerate(unit)}
    df_los = df_data[df_data.reviewDate.dt.year == int(year)].groupby('month')['lengthOfStay'].mean().round('D').reset_index()
    # df_los['month'] = df_los.month.map(val)
    df_los['lengthOfStay'] = df_los['lengthOfStay'].dt.days
    # df_los = df_los.sort_values('')
    # ax2.bar()
    # sns.lineplot(data=df,x='reviewDate', y='ratingSummary', marker='o',ax=ax)
    # ax2=ax.twinx()
    sns.histplot(
        df_data[df_data.reviewDate.dt.year == int(year)], 
        # palette = sns.color_palette("ch:start=.2,rot=-.3"),
        x='month',hue='tripType', multiple='stack', alpha=0.5,ax=ax)
    ax.set_ylabel('Booking Frequency', fontsize=16)
    ax.set_xlabel('Month', fontsize=16)
    ax2=ax.twinx()
    sns.lineplot(data=df_los, x='month', y='lengthOfStay',color='blue',marker='o', ax=ax2)
    ax2.set_ylabel('Average Length of Stay', fontsize=16)

    ax.get_legend().set_title("Trip Types")
    
    return fig, ax


def rating_count(df_data, by):
    fig,ax = plt.subplots(figsize=(15,12))
    df = df_data.sort_values('reviewDate')
    # df['days']
    df['month']=df.reviewDate.dt.month
    if by == 'date':
        ax.plot(df['reviewDate'].values, df['ratingSummary'].values, marker='o')
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.xticks(rotation=45)
    elif by == 'month':
        d = df.groupby(df.reviewDate.dt.month)['ratingSummary'].mean().reset_index()
        ax.plot(d['reviewDate'].values, d['ratingSummary'].values, marker='o')
    elif by == 'year':
        d = df.groupby(df.reviewDate.dt.year)['ratingSummary'].mean().reset_index()
        ax.plot(d['reviewDate'].values, d['ratingSummary'].values, marker='o')

    ax.set_xlabel(by.capitalize()+'s')
    ax.set_ylabel('Ratings')
    ax.set_ylim((0,5.3))
    
    return fig, ax

# 
def stay_review(df, year):
    # df_melt = pd.melt(df, id_vars=['tripType'], var_name='trip', value_name='tripval')
    fig, ax = plt.subplots(figsize=(15,12))
    df['month'] = df['reviewDate'].dt.month
    df['day'] = df.lengthOfStay.dt.days
    df_data = df[df.reviewDate.dt.year == int(year)].groupby(['month','tripType'])[['ratingSummary','day']].mean().reset_index()#.set_index('month')
    # print(df_data)
    df_pivot =df_data.pivot(index='month', columns='tripType', values='ratingSummary')#.sort_values()
    df_data2 = df[df.reviewDate.dt.year == int(year)].groupby(['month','tripType'])[['lengthOfStay']].mean().reset_index()
    df_pivot2 =df_data2.pivot(index='month', columns='tripType', values='lengthOfStay')
    print(df_data2)
    print(df_pivot2)
    # fig, ax = plt.subplot(figsize=(12,12))
    # print(df_pivot)
    # df_data = df[df.reviewDate.dt.year == int(year)].groupby(['month'])['lengthOfStay'].mean().reset_index()#.set_index('month')
    # df_data = df_data.sort_values('month')
    # ax.plot(df_data['month'],df_data['lengthOfStay'], 'go-')
    # # sns.lineplot(data=df_data, x='month', y='lengthOfStay',color='blue',marker='o', ax=ax)
    # ax.set_xticks(range(1,13))
    # ax.set_xticklabels(range(1,13))
    print(df_pivot2)
    # ax.set_xlim(1,12)
    print(df_pivot)
    df_pivot.fillna(0, inplace=True)
    # df_pivot.plot(kind='bar', stacked=True, ax=ax, position=np.arange(len(df_pivot.index)))
    sns.barplot(data=df_data, x='month', y='day', hue="tripType", ax=ax)
    ax.set_ylabel("Days of Stay",fontsize=16)
    ax2 = ax.twinx()
    sns.barplot(data=df_data, x='month', y='ratingSummary', hue="tripType", ax=ax2)
    ax2.set_ylabel("Ratings",fontsize=16)
    ax.set_xlabel("Month", fontsize=16)
    ax2.get_legend().set_title("Trip Types")
    
    return fig,ax



