import flask, os, json
from flask import request, jsonify
import pandas as pd
from datetime import datetime, timedelta
import pytz
from Webscraper_tools.Webscrape import scrape_cnbc, scrape_cnn, save_df
from Webscraper_tools.Watsonx_connection import *
from Webscraper_tools import single_bullet_prompt
from flask_cors import CORS
from data.database import Database

pickle_path = "./data/articles.pickle"
boundary = datetime.now(tz=pytz.timezone("US/Eastern")) - timedelta(days=1)

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
db = Database()

def update_db() :

    cnn_articles = scrape_cnn()
    cnbc_articles = scrape_cnbc()
    articles = cnn_articles + cnbc_articles

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
    get_full_summary(df)
    place_ticker_batch(df)

    data_for_insert = []
    for _, row in df.iterrows() :
        if not db.check_exists(['Title']) :
            data_for_insert.append(row['Source'], row['Title'], row['Text'], row['Date'], row['Link'], row['Category'], row['Summary'])

    db.add(data_for_insert)


    

update_db()
print("READY")

### FLASK ROUTES

@app.route("/article")
def get_article() :
    body = request.get_json()
    index = body.get("article_id", -1)
    result = db.get(index)
    if result is not None :
        return result, 200
    else :
        return "Error retrieving article", 403

@app.route("/today")
def get_today_news() :
    today_rows = db.get_today()
    if len(today_rows) > 0 :
        cat_map = {}
        cat_list = []
        for article in today_rows :
            #print("Category: " + cat)
            cat = article['category']
            if cat == 'nan' or cat is None :
                continue
            cat_map[cat] = {"category": cat, "summaries": []}
            if article["summary"] :
                cat_map[cat]['summaries'].append(article["summary"])
        
        for cat_dict in cat_map.values() :
            cat_list.append(cat_dict)

        return json.dumps(cat_list), 200
    else :
        return "No news today!", 400

@app.route("/all")
def get_all() :
    return db.get_all(), 200
    
@app.route("/refresh", methods=['POST'])
def refresh() :
    update_db()