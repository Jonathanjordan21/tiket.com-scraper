from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from matplotlib.pyplot import Line2D

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

    fig, ax = plt.subplots(figsize=(12,12))

    try :
        h = df.groupby(['tripType']).count()['ratingSummary'].sort_values()
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
    except :
        return fig,ax.axis('off')

def customer_count(df_data, year):
    # print(year)
    fig, ax = plt.subplots(figsize=(12,12))
    try :
        df_data = df_data.sort_values('reviewDate')
        df_data['month']=df_data.reviewDate.dt.month
        # print(df_data['month'].unique())
        
        # print(df_data['month'].unique())
        # unit = ['dec','jan','feb','mar','apr','may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        # val = {i:u for i,u in enumerate(unit)}
        df_los = df_data[df_data.reviewDate.dt.year == int(year)].groupby('month')['lengthOfStay'].mean().round('D').reset_index()
        # df_los['month'] = df_los.month.map(val)
        df_los['lengthOfStay'] = df_los['lengthOfStay'].dt.days
        # df_los = df_los.sort_values('')
        # ax2.bar()
        # sns.lineplot(data=df,x='reviewDate', y='ratingSummary', marker='o',ax=ax)
        # ax2=ax.twinx()
    
        sns.histplot(
            df_data[df_data.reviewDate.dt.year == int(year)], 
            palette = "Set1",
            x='month',hue='tripType', multiple='stack', alpha=0.5,ax=ax)
        ax.set_ylabel('Booking Frequency', fontsize=16)
        ax.set_xlabel('Month', fontsize=16)
        ax2=ax.twinx()
        sns.lineplot(data=df_los, x='month', y='lengthOfStay',color='blue',marker='o', ax=ax2)
        ax2.set_ylabel('Average Length of Stay', fontsize=16)

        ax.get_legend().set_title("Bookings")
        xtick = [x for x in range(1,13)]
        map_xtick = {i+1:u for i,u in enumerate(['Jan','Feb','Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}
        print(ax.get_xticks())
        ax.set_xticklabels([map_xtick.get(x) for x in ax.get_xticks()])
    except :
        ax.axis('off')
        pass
    
    return fig, ax


def rating_count(df_data, by):
    fig,ax = plt.subplots(figsize=(15,12))
    df = df_data.sort_values('reviewDate')
    # df['days']
    df['month']=df.reviewDate.dt.month
    try :
        if by == 'date':
            ax.plot(df['reviewDate'].values, df['ratingSummary'].values, marker='o')
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            plt.xticks(rotation=45)
        elif by == 'month':
            d = df.groupby(df.reviewDate.dt.month)['ratingSummary'].mean().reset_index()
            # sns.lineplot(d, x='reviewDate', y='ratingSummary', hue=df.reviewDate.dt.year,markers='o')
            ax.plot(d['reviewDate'].values, d['ratingSummary'].values, marker='o')
            # xtick = [x for x in range(1,13)]
            try :
                map_xtick = {i:u for i,u in enumerate(['Jan','Feb','Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}
                ax.set_xticklabels([map_xtick.get(x) for x in ax.get_xticks()])
            except :
                pass
        elif by == 'year':
            d = df.groupby(df.reviewDate.dt.year)['ratingSummary'].mean().reset_index()
            ax.plot(d['reviewDate'].values, d['ratingSummary'].values, marker='o')

        ax.axhline(df['ratingSummary'].mean(), color='grey', linestyle='dashed', label='Total Average')
        h, l = ax.get_legend_handles_labels()
        line_legend = Line2D([0],[0],color='green',linestyle='--', label='Total Average')
        h.append(line_legend)
        l.append('Total Average')
        ax.set_xlabel(by.capitalize()+'s', fontsize=16)
        ax.set_ylabel('Ratings', fontsize=16)
        ax.set_ylim((0,5.3))
    except:
        pass
    return fig, ax

# 
def stay_review(df, year):
    # df_melt = pd.melt(df, id_vars=['tripType'], var_name='trip', value_name='tripval')
    fig, ax = plt.subplots(figsize=(15,12))
    df['month'] = df['reviewDate'].dt.month
    df['day'] = df.lengthOfStay.dt.days
    try :
        df_data = df[df.reviewDate.dt.year == int(year)].groupby(['month','tripType'])[['ratingSummary','day']].mean().reset_index()#.set_index('month')
        # print(df_data)
        df_pivot =df_data.pivot(index='month', columns='tripType', values='ratingSummary')#.sort_values()
        df_data2 = df[df.reviewDate.dt.year == int(year)].groupby(['tripType'])[['lengthOfStay']].mean().reset_index()
        # df_pivot2 =df_data2.pivot(index='month', columns='tripType', values='lengthOfStay')
        
        
        df_pivot.fillna(0, inplace=True)
        # df_pivot.plot(kind='bar', stacked=True, ax=ax, position=np.arange(len(df_pivot.index)))
        
        ax2 = ax.twiny()
        
        sns.barplot(data=df_data, x='ratingSummary', y='month', hue="tripType", ax=ax, orient='h', color='darkblue')#, alpha=[0.7]*len(df_data2.index))#, label='Rating')
        for bar in ax.containers[0]:
            bar.set_alpha(0.6)
        sns.barplot(data=df_data, x='day', y='month', hue="tripType", ax=ax2, orient='h', color='darkred')#, label='Length Of Stay')
        ax.set_xlabel("Average Ratings",fontsize=16)
        ax2.set_xlabel("Average Days of Stay",fontsize=16)
        ax.set_ylabel("Month", fontsize=16)
        # ax2.yaxis().set_visible(False)

        map_ytick = {i:u for i,u in enumerate(['Jan','Feb','Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])}
        ax.set_yticklabels([map_ytick[y] for y in ax.get_yticks()])
        
        # ax2.get_legend().set_title("(Blue) Rating")
        # ax.get_legend().set_title("(Red) Length Of Stay")
        ax2.legend(fontsize=14,title = "Length of Stay", loc='upper center', bbox_to_anchor=(0.3,-0.05))
        ax.legend(fontsize=14,title = "Rating", loc='upper center', bbox_to_anchor=(0.7,-0.05))

        ax.axvline(df_data['ratingSummary'].mean(), color='b', linestyle='dashed', label='Total Average Rating')

        ax2.axvline(df_data['day'].mean(), color='r', linestyle='dashed', label='Total Average Length of Stay')
        # ax2.get_legend().set_fontsize(14)
        # ax.get_legend().set_fontisize(14)
        
    except:
        ax.axis('off')
        pass
    
    return fig,ax


def trip_types(df):
    fig,ax = plt.subplots(figsize=(12,12))
    
    try :
        df['day'] = df.lengthOfStay.apply(lambda x:x.total_seconds()/86400)
        type_list = [x for x in df.columns if 'Rating_' in x]
        df2 = df.groupby('tripType')[type_list+['ratingSummary']].mean().reset_index()

        df3 = pd.melt(df2, id_vars=['tripType','ratingSummary'],var_name='ratingType', value_name='ratingVal')

        baseline=df3['ratingSummary'].mean()
        df3['ratingVal'] = df3['ratingVal']-baseline
        sns.barplot(
            data=df3,x='ratingVal',y='ratingType', hue='tripType',
            orient='h',left=baseline, palette=sns.color_palette('coolwarm')
        )
        
        ax.axvline(baseline, color='green', linestyle='dashed', label='Total Average')
        
    except Exception as e:
        print(e)
        ax.axis('off')
    
    return fig,ax



