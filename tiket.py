import streamlit as st
import pandas as pd
from datetime import datetime
from components import extract, load, transform, visualize
import os

@st.cache_resource
def installff():
    os.system('curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
    os.system('dpkg -i google-chrome-stable_current_amd64.deb')
    os.system('!wget https://chromedriver.storage.googleapis.com/2.46/chromedriver_linux64.zip')
    os.system('!unzip chromedriver_linux64.zip')
    os.system('chmod +x chromedriver')
    os.system('mv -f chromedriver /home/appuser/venv/bin/chromedriver')
    os.system('sbase get chromedriver latest')
    os.system('sbase get chromedriver 107')
    os.system('sbase install chromedriver latest')
    
    os.system('sbase get chromedriver latest')
    os.system('sbase get chromedriver latest-1')
    os.system('chmod +x chromedriver')
    os.system('chmod 777 chromedriver')
    # os.system('chmod 777')
    os.system('chmod 777 /home/adminuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/chromedriver-linux64.zip')
    os.system('chmod +x /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/chromedriver')
    os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')

_ = installff()



st.title("Reviews Analyzer (tiket.com)")
st.divider()
st.markdown("""<div style="text-align: center;">
<p style="color:yellow;">Warning : <br>
This is only for educational purposes<br>
Unethically Scraping data from tiket.com is illegal by law<br>
Please read the robots.txt in tiket.com for further information</p></div>
""", unsafe_allow_html=True)

oo = []
# opt = (f_name)
opt = {}
# st.session_state['df']= pd.DataFrame()

    # out.append([df, f_name])
if 'opt' not in st.session_state:
    st.session_state.opt = {} 
# @st.cache()
# def get_opt():
#     return list(opt.keys())
if 'hotel' not in st.session_state:
    st.session_state.hotel = []

# if 'list_df' not in st.session_state:

if 'cur_df' not in st.session_state:
    st.session_state.cur_df = pd.DataFrame()

if 'cur_questions' not in st.session_state:
    st.session_state.cur_questions = []

if 'extract_progress' not in st.session_state:
    st.session_state.extract_progress = 0

if 'states' not in st.session_state:
    st.session_state.session_state = False

if 'year' not in st.session_state:
    st.session_state.year = str(datetime.now().year)

if 'dates' not in st.session_state:
    st.session_state.dates = 'date'

if 'states' not in st.session_state:
    st.session_state.states = False

if 'disabled' not in st.session_state:
    st.session_state.disabled = True

if 'dis' not in st.session_state:
    st.session_state.dis = False

@st.cache_resource
def convert_df(df):
    return df.to_csv().encode('utf-8')


url = st.text_input("Tiket.com Reviews Url")
st.text("Example : https://www.tiket.com/review?product_type=TIXHOTEL&searchType=INVENTORY&inventory_id=neo-denpasar-108001534490316188&reviewSubmitColumn=RATING_SUMMARY&hideToolbar=null")
st.markdown("""<div style="text-align: center;">
<p style="color:yellow;">Note : Extracting data often fail due to page redirection</p></div>
""", unsafe_allow_html=True)

def disable():
    st.session_state.dis = True

if st.button(label="Extract Reviews Data",on_click=disable, disabled=st.session_state.get('dis',True)):
    if url != "":
        st.write("Extracting data...")
        try :
            dict_name, driver,total_reviews, total_pages = extract.scrape_reviews(url.strip())
            st.session_state.hotel.append(dict_name)
            # st.progress(st.session_state.extract_progress, f'{st.session_state.extract_progress*100}%')
            # st.write("Done!")for n in range(1,l+1):
            # ns = extract.
            # for x in extract.scrape_pages(dict_name, driver, total_pages):
                # st.session_state.extract_progress+=100/total_pages
            #     n_data = x
            st.session_state.disabled = False
            bar = st.progress(0)
            m=0
            try :
                for n in range(1,total_pages+1):
                    m = extract.scrape_one_page(dict_name, driver, n)
                    bar.progress(m/total_pages)
            except Exception as e:
                driver.quit()
                st.write("The operation cancelled on the way!")
            n_data = m*5
            st.session_state.dis = False

            # n_data = extract.scrape_pages(f_name, driver)
            if n_data < total_reviews:
                st.write("Oops! the operation might be corrupted!")
                st.write(f"You have sucessfully downloaded {n_data} reviews out of {total_reviews}")
                st.write(f"If you're not fine with this, please re-download the review data")
            else :
                st.write(f"Congratulations! You have sucessfully downloaded {total_reviews} reviews out of {total_reviews}")
            driver.quit()

        except Exception as e:
            st.write(e)
            st.session_state.dis = False
            st.write("Oops! Something's Wrong! Please check the url")
    else :
        st.session_state.dis = False
        st.write("The Url Link is Empty!")



def change_hotel():
    st.write("Loading data...")
    cur_df, questions = load.load_data(data_name)
    st.write("Cleaning data...")
    st.session_state.cur_df, st.session_state.cur_questions = transform.clean_data(cur_df, questions)
    # st.session_state.cur_questions = [x.replace('Rating_') for x in st.session_state.cur_questions]
    st.write("Done!")
    st.session_state.states = True

    st.download_button(
        label="Download data csv",
        data=convert_df(st.session_state.cur_df),
        file_name=f'{data_name}.csv',
        mime='text_csv'
    )

data_name = st.selectbox(
    label="Choose Review Data",
    options=set(st.session_state.hotel),
    on_change=change_hotel
)


if st.button(label="Refresh Table", disabled=st.session_state.get('disabled', True)):
    # print(opt)
    st.write("Loading data...")
    try :
        cur_df, questions = load.load_data(data_name)
        st.write("Cleaning data...")
        st.session_state.cur_df, st.session_state.cur_questions = transform.clean_data(cur_df, questions)
        # st.session_state.cur_questions = [x.replace('Rating_') for x in st.session_state.cur_questions]
        st.write("Done!")
        
        st.session_state.states = True

        st.download_button(
            label="Download data csv",
            data=convert_df(st.session_state.cur_df),
            file_name=f'{data_name}.csv',
            mime='text_csv'
        )
    except:
        st.write("Something Wrong! Please Re-Extract the Data")



def trip_type_pie(df):
    st.header("Bookings per Types of Visit")
    fig, ax = visualize.pie_chart(df)
    st.pyplot(fig)

def wordcloud(df):
    st.header("WordCloud of Customers' Comments")
    stop_words = st.text_input("Add Stopwords List (Comma separated)")
    st.text("Example : hotel,bangun,kolam,berenang")
    st.text("Stopwords are used to remove the frequent but non-important words")
    
    fig, ax = visualize.wordcloud(df, [x.strip() for x in stop_words.split(",")])
    st.pyplot(fig)

def customer_count_chart(df):
    st.header("Booking Frequency & Length of Stay")
    options = list(df.startJourney.dt.year.unique().astype('str'))
    # print('a')
    year = st.selectbox("Select Year", options=options, key='year')
    # print('anto')
    fig,ax=visualize.customer_count(df, year)
    
    st.pyplot(fig)

def rating_chart(df):
    st.header("Average Ratings Overtime")
    # def change_rating(op):
    # options = list(df.reviewDate.dt.year.unique().astype('str'))
    # if 'year3' not in st.session_state:
    #     st.session_state.year3 = str(datetime.now().year)
    # year = st.selectbox("Select Year", options=options, key='year3')
    option = ['date', 'month', 'year']
    # st.session_state.dates = option.index('date')
    date = st.selectbox("Select Range", options=option, key='dates')
    # st.session_state.dates = date
    fig,ax = visualize.rating_count(df, date)
    st.pyplot(fig)

def los_review(df):
    st.header('Average Length of Stay & Reviews per Month')
    options = list(df.reviewDate.dt.year.unique().astype('str'))
    if 'year2' not in st.session_state:
        st.session_state.year2 = str(datetime.now().year)
    year = st.selectbox("Select Year", options=options, key='year2')
    fig, ax = visualize.stay_review(df, year)

    st.pyplot(fig)

def trip_types_chart(df):
    st.header('Rating Details')
    fig, ax = visualize.trip_types(df)
    st.pyplot(fig)


if st.session_state.states:
    df_str = st.session_state.cur_df.copy()
    df_str['lengthOfStay'] = df_str['lengthOfStay'].astype('str')
    st.dataframe(df_str)
    # with st.form("visualization"):
    st.header("Visualization")
    col1,col2,col3 = st.columns(3)
    with col2:
        if 'slid' not in st.session_state:
            st.session_state.slid = (1,5)
        slid = st.slider("Rating", min_value=1, max_value=5, key='slid')

        if 'stay' not in st.session_state:
            st.session_state.stay = (1,15)
        stay = st.slider("Length of Stay", min_value=0, max_value=30, key='stay')
        
    with col1:
        opts = list(st.session_state.cur_df['tripType'].unique())
        if 'trip' not in st.session_state:
            st.session_state.trip = list(opts)
        trip = st.multiselect("Types of Visit", options=opts, key="trip")
        
    with col3:
        st.text("Latest Review Date")
        if 'startdate' not in st.session_state:
            st.session_state.startdate = st.session_state.cur_df['reviewDate'].dt.date.min()
        if 'enddate' not in st.session_state:
            st.session_state.enddate = datetime.now().date()
        startdate=st.date_input("Start Date", key='startdate')
        enddate=st.date_input("End Date", key='enddate')

    # submitted = st.form_submit_button("Refresh Visuals")
    
    # if submitted:
    df = transform.filter_df(
        st.session_state.cur_df, slid, trip, startdate, enddate, stay
    )
    

    wordcloud(df)
    trip_type_pie(df)
    customer_count_chart(df)
    los_review(df)
    rating_chart(df)
    trip_types_chart(df)


    














# def generate_table():
#     with open("net_0.json", "r") as f:
#         data1 = json.loads(json.loads(f.read())['body'])['data']
#     with open("net_1.json", "r") as f:
#         data2 = json.loads(json.loads(f.read())['body'])['data']
    
#     df1_data1 = pd.DataFrame(data1['content'])
#     df2_data1 = pd.DataFrame(data1['comments'])
#     df_data1 = df1_data1.join(df2_data1[['reviewId','value']].set_index('reviewId'), on='reviewId')
#     df_data1.rename(columns={'value':'comment'}, inplace=True)
#     df_data1.drop_duplicates(subset=['reviewId'], inplace=True)

#     df_data2 = pd.DataFrame(data2['userReviews']['content'])[['customerName','reviewDate','ratingSummary']]
#     df_data2['comment'] = [x['comments'][0]['value'] for x in data2['userReviews']['content']]
#     df = pd.concat([df_data1,df_data2], ignore_index=True)
    # df['ratingSummary'] = df['ratingSummary'].astype('float32')
    # df['reviewDate'] = df['reviewDate'].apply(lambda x : datetime.fromtimestamp(int(x)/1000))
#     return df.loc[:, ~df.columns.isin(['reviewId', 'imageUrl'])]

# df = generate_table()
# url = "https://www.tiket.com/review?product_type=TIXHOTEL&searchType=INVENTORY&inventory_id=neo-denpasar-108001534490316188&reviewSubmitColumn=RATING_SUMMARY&hideToolbar=null"



