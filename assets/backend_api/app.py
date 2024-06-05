import flask, os, json
from flask import request, jsonify
import pandas as pd
from datetime import datetime, timedelta
import pytz
from Webscraper_tools.Webscrape import scrape_cnbc, scrape_cnn, save_df
from Webscraper_tools.Watsonx_connection import *
from Webscraper_tools import single_bullet_prompt
from flask_cors import CORS

pickle_path = "./data/articles.pickle"
boundary = datetime.now(tz=pytz.timezone("US/Eastern")) - timedelta(days=1)

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def create_df() :

    cnn_articles = scrape_cnn()
    cnbc_articles = scrape_cnbc()
    articles = cnn_articles + cnbc_articles

    sources_lst = []
    title_lst = []
    text_lst = []
    date_lst = []
    link_lst = []
    #check first if a pickle file exists
    if os.path.isfile(pickle_path) :
        df = pd.read_pickle(pickle_path)
        for article in articles :
            if article[1] not in df['Title'].unique() : #if this is a new article, add it
                sources_lst.append(article[0])
                title_lst.append(article[1])
                text_lst.append(article[2])
                date_lst.append(article[3])
                link_lst.append(article[4])

        if len(title_lst) == 0 :
            return df

        #now we need to do the llm stuff on the new articles
        #CATEGORIES
        categories_text = get_categories_backend(title_lst)
        try :
            categories = json.loads(categories_text)
        except Exception as e:
            raise Exception(f"Category retrieval failed! Error: {str(e)}")
        
        #CONVERT CATEGORIES DICT INTO A LIST OF CATEGORIES
        cat_lst = [None] * len(title_lst)
        print(f"Article count: {len(title_lst)}")
        for key in categories.keys() :
            for index in categories[key] :
                cat_lst[index - 1] = key

        #BULLET SUMMARIES
        prompts = []
        for i in range(len(title_lst)) :
            articleTitle = title_lst[i]
            articleText = text_lst[i]
            prompts.append(Prompt_Input_Single_Bullet(single_bullet_prompt, articleTitle, articleText))
    
        BAM_Response = Query_BAM_Batch(prompts, 200)
        summary_lst = [None] * len(title_lst)
        for i in range(len(title_lst)) :
            summary_lst[i] = BAM_Response[i][0].text.replace("---", "").replace("\n", "").replace("Summary: ", "").replace("  ", "")


        #FORM THE MERGED DATAFRAME
        dct = {
            'Source': sources_lst,
            'Title' : title_lst,
            'Text': text_lst,
            'Date': date_lst,
            'Link': link_lst,
            'Category': cat_lst,
            'Summary': summary_lst
        }
        df_to_concat = pd.DataFrame(dct)
        return pd.concat([df, df_to_concat], ignore_index=True)

    #If there is no df that already exists
    else :
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

    
        return df

df = create_df()
place_ticker_batch(df)
save_df(df)
print("READY")

### FLASK ROUTES

@app.route("/article")
def get_article() :
    body = request.get_json()
    index = body.get("article_id", -1)
    if index not in df.index :
        return "Invalid index", 400
    else :
        return df.iloc[index].to_json(), 200

@app.route("/today")
def get_today_news() :
    today_rows = df.loc[(df["Date"] > boundary)]
    if today_rows.shape[0] > 1 :
        cat_list = []
        for cat in today_rows.Category.unique() :
            #print("Category: " + cat)
            if cat == 'nan' or cat is None :
                continue
            cat_rows = today_rows.loc[(today_rows["Category"] == cat)].iterrows()
            cat_dict = {"category": cat, "summaries": []}
            for _, article in cat_rows :
                if article["Summary"] :
                    cat_dict['summaries'].append(article["Summary"])
            cat_list.append(cat_dict)

        return json.dumps(cat_list), 200
    else :
        return "No news today!", 400

@app.route("/all")
def get_all() :
    if df.shape[0] > 1 :
        return df.to_json(), 200
    else :
        return "Dataframe is empty", 400
    
@app.route("/refresh", methods=['POST'])
def refresh() :
    global df
    df = create_df()
    save_df(df)
