import requests
from bs4 import BeautifulSoup
import re
from dateutil import parser
import pandas as pd
from .util import remove_formatting
import streamlit as st


#CNN
@st.cache_data
def scrape_cnn() :
    cnn_URL = "https://www.cnn.com/business"
    cnn_page = requests.get(cnn_URL)

    cnn_soup = BeautifulSoup(cnn_page.content, "html.parser")
    cnn_articles = cnn_soup.find_all('div', {'class': 'container_lead-plus-headlines-with-images__item'})

    cnn_links = []
    for article in cnn_articles :
        if not any(avoided in article['data-open-link'] for avoided in ['live', 'videos']) : #skip live articles and videos for now they have a different format
            cnn_links.append("https://www.cnn.com" + article['data-open-link'])
    
    cnn_articles= []

    for link in cnn_links:

        page = requests.get(link)

        content = ""
        soup = BeautifulSoup(page.content, "html.parser")
        cnn_title = soup.find('h1', {'class': 'headline__text inline-placeholder'})
        cnn_content = soup.find('div', {'class': 'article__content-container'})
        for p in cnn_content.find_all('p', {'class': 'paragraph inline-placeholder'}) :
            content = content + " " + p.text
        timestamp = soup.find('div', {'class': 'timestamp'})
        timestr = timestamp.text
        digits = re.search(r"\d", timestr)
        dt = parser.parse(timestr[digits.start(0):])

        try :
            cnn_articles.append(['CNN', remove_formatting(cnn_title.text),remove_formatting(content), dt, link])
        
        except:
            print("This article has no text!")
    
    return cnn_articles



#CNBC
@st.cache_data
def scrape_cnbc() :
    cnbc_URL = "https://www.cnbc.com/business/"
    cnbc_page = requests.get(cnbc_URL)

    cnbc_soup = BeautifulSoup(cnbc_page.content, "html.parser")
    cnbc_articles = cnbc_soup.find_all('a', {'class': 'Card-title'}, href=True)

    cnbc_links = []
    for article in cnbc_articles :
        cnbc_links.append(article['href'])

    cnbc_articles= []

    for clink in cnbc_links :
        page = requests.get(clink)

        soup = BeautifulSoup(page.content, "html.parser")

        content = ""
        cnbc_title = soup.find('h1', {'class': 'ArticleHeader-headline'})
        cnbc_content = soup.find('div', {'class': 'ArticleBody-articleBody'})
        for div_group in cnbc_content.find_all('div', {'class': 'group'}) :
            for p in div_group.find_all('p') :
                content = content + " " + p.text
        cnbc_time = soup.find('time', {'itemprop': 'datePublished'})
        dt = parser.parse(cnbc_time['datetime'])

        try :
            cnbc_articles.append(['CNBC', remove_formatting(cnbc_title.text), remove_formatting(content), dt, clink])
        except:
            print("This article has no text!")

    return cnbc_articles

def create_df(articles) :
    sources_lst = []
    title_lst = []
    text_lst = []
    date_lst = []
    link_lst = []

    for i in range(len(articles)) :
        sources_lst.append(articles[i][0])
        title_lst.append(articles[i][1])
        text_lst.append(articles[i][2])
        date_lst.append(articles[i][3])
        link_lst.append(articles[i][4])
    
    dct = {
    'Source': sources_lst,
    'Title' : title_lst,
    'Text': text_lst,
    'Date': date_lst,
    'Link': link_lst
    }

    df = pd.DataFrame(dct)

    #Intialize the dataframe to add the 5 extra columns
    _, row_len = df.shape
    cols_to_add = ["Country", "Interest Rate", "Consumer Spending", "Production", "Employment", "Inflation", "NetSentiment"]
    for i in range(len(cols_to_add)) :
        df.insert(row_len, cols_to_add[i], None)
        row_len += 1

    #run_llm(df)
    
    return df

@st.cache_resource(show_spinner="Retrieving articles")
def do_webscrape() :
    cnn_articles = scrape_cnn()
    cnbc_articles = scrape_cnbc()
    combined_articles = cnn_articles + cnbc_articles

    return create_df(combined_articles)

