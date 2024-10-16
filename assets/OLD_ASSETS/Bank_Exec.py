import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import pytz
from Webscraper_tools.Webscrape import *
from Webscraper_tools.Watsonx_connection import single_article_summary, get_full_summary, place_ticker_batch
from Webscraper_tools.ticker_api import get_ticker_from_name
from menu import menu

st.set_page_config(layout="wide")
st.title("News Analysis with watson:blue[x]")

boundary = datetime.now(tz=pytz.timezone("US/Eastern")) - timedelta(days=1)

def refresh() :
   do_webscrape.clear()
   scrape_cnbc.clear()
   scrape_cnn.clear()
   st.session_state["summary_try"] = False



def render_df() :
   datfram = pd.DataFrame(df.iloc[st.session_state['article_id'], 4:12]).T
   _, num_cols = datfram.shape
   sentiment_to_emoji = {"Falling": ":arrow-down-small:", "Decrease": ":arrow-down-small:", "Worse": ":arrow-down-small:", "Worst": ":arrow-down-small:", "Increase": ":arrow-up-small:", "Rising": ":arrow-up-small:", "Better": ":arrow-up-small:"} 
   for i in range(num_cols) :
      if datfram.iloc[0, i] in sentiment_to_emoji.keys() :
         datfram.iloc[0, i] = datfram.iloc[0, i] + " " + sentiment_to_emoji[datfram.iloc[0, i]]
   st.dataframe(datfram)

# tab1, tab2 = st.tabs(['CNN', 'CNBC'])


topcol1, topcol2 = st.columns([.85, .1])
with topcol2 :
   st.button("Refresh Webscrape", on_click=refresh, key="refresh_button")

if "role" not in st.session_state or st.session_state.role is None:
   st.session_state.role = "bank"


#Program
df = do_webscrape()
num_articles, _ = df.shape
if "summary_success" not in st.session_state :
   st.session_state["summary_success"] = False

#Summary Dashboard
if "summary_try" not in st.session_state or not st.session_state["summary_try"]:
   st.session_state["summary_try"] = False
   st.session_state['got_companies'] = [0] * num_articles
   st.session_state["summary_success"] = get_full_summary(df)
   st.session_state["summary_try"] = True

if 'got_companies' not in st.session_state or not st.session_state['got_companies'] :
   st.session_state['got_companies'] = False

#Edit summaries to include company links
if st.session_state['summary_success'] and not any(st.session_state['got_companies']) :
   place_ticker_batch(df)
   

#display the dashboard
if st.session_state['summary_success'] :
   for cat in df.Category.unique() :
      #print("Category: " + cat)
      if cat == 'nan' or cat is None :
         continue
      
      cat_rows = df.loc[(df["Category"] == cat) & (df["Date"] > boundary)].iterrows()
      wrote_category = False
         
      for index, row_in_category in cat_rows :
         if not wrote_category : #just only write the category if its necessary
            st.write("**" + str(cat) + "**")
            wrote_category = True
         #print(row_in_category)
         if row_in_category["Summary"] :
            summ = row_in_category["Summary"]     
            st.write(summ)
                  
else :
   st.write("Summary retrieval failure")

save_df(df)
menu()
      