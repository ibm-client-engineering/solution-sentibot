import pandas as pd
import streamlit as st
import time
from Webscraper_tools.Webscrape import *
from Webscraper_tools.Watsonx_connection import single_article_summary, get_full_summary
from menu import menu

st.set_page_config(layout="wide")
st.title("News Analysis with Watson:blue[x]")


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

#Summary Dashboard (commented out for now the prompting is broken)
if "summary_try" not in st.session_state or not st.session_state["summary_try"]:
   st.session_state["summary_try"] = True
   st.session_state["summary_success"] = get_full_summary(df)

if st.session_state['summary_success'] :
   for cat in df.Category.unique() :
      #print("Category: " + cat)
      st.write("**" + str(cat) + "**")
      cat_rows = df.loc[df["Category"] == cat].iterrows()
      for index, row_in_category in cat_rows :
         #print(row_in_category)
         if row_in_category["Summary"] :
            st.write("- " + row_in_category["Summary"])
else :
   st.write("Summary retrieval failure")

menu()
      