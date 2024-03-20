import streamlit as st
import pandas, time
from Webscraper_tools.Webscrape import do_webscrape, scrape_cnbc, scrape_cnn
from Webscraper_tools.Watsonx_connection import single_article_summary
from menu import menu


def populate_columns() : 
   st.session_state['selected'] = True
   st.session_state['button_clicked'] = False

#Column populating function
def article_click(article_id) :
   st.session_state['button_clicked'] = True
   st.session_state['article_id'] = article_id

def refresh() :
   do_webscrape.clear()
   scrape_cnbc.clear()
   scrape_cnn.clear()
   st.session_state["summary_try"] = False

def run_wx_single(df, i) :
   start_time = time.time()
   st.session_state['analysis_run'][i] = 1
   with col2:
      with st.spinner("Doing watson:blue[x] analysis") :
         single_article_summary(df, i)
      st.success(f"Completed Analysis in {time.time() - start_time} seconds", icon="✅")

if 'selected' not in st.session_state :
   st.session_state['selected'] = False
if 'button_clicked' not in st.session_state :
   st.session_state['button_clicked'] = False
if 'article_id' not in st.session_state :
   st.session_state['article_id'] = -1

topcol1, topcol2 = st.columns([.85, .1])
with topcol2 :
   st.button("Refresh Webscrape", on_click=refresh, key="refresh_button")

#get df
df = do_webscrape()
num_articles, _ = df.shape

st.selectbox("Select a news source", ("CNN", "CNBC"), on_change=populate_columns, key="source_selection", index=None, placeholder="News Source")
col1, col2 = st.columns([.3, .7])
if 'analysis_run' not in st.session_state :
   st.session_state['analysis_run'] = [0] * num_articles

if st.session_state['selected'] :
    source_df = df.loc[df['Source'] == st.session_state['source_selection']]
    with col1:
        st.title("Headlines")
        with st.container(height=600, border=False) :
            for index, row in source_df.iterrows() :
                if index == st.session_state['article_id'] :
                    st.button(row['Title'], on_click=article_click, args=(index,), type='primary')
                else:
                    st.button(row['Title'], on_click=article_click, args=(index,))

if st.session_state['button_clicked'] :
    with col2:
      st.subheader(df.iloc[st.session_state['article_id']]['Title'])
      st.caption(df.iloc[st.session_state['article_id']]['Date'].strftime('Published %B %d, %Y at %I:%M %p %Z'))
      st.write(df.iloc[st.session_state['article_id']]['Text'])
      if st.session_state['analysis_run'][st.session_state['article_id']] == 1 :
         #render_df()
         df.iloc[st.session_state['article_id']]['Multi-Point Summary']
      else :
         st.button("Run Watson:blue[x] Analysis", on_click=run_wx_single, args=(df, st.session_state['article_id']))

menu()