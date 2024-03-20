from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models import Model
import requests
import json
from .util import update_row_with_dict, get_net_sentiment
from Webscraper_tools import prompt, single_article_summary_prompt, categories_prompt, single_bullet_prompt
import traceback
from genai.client import Client
from genai.credentials import Credentials
from genai.schema import (
    DecodingMethod,
    ModerationStigma,
    ModerationParameters,
    TextGenerationParameters,
)
from langchain_core.callbacks.base import BaseCallbackHandler
from genai.extensions.langchain import LangChainInterface
from tqdm.auto import tqdm
import streamlit as st

BAM_API_Key = ""
BAM_URL = ""
model_id = "ibm-mistralai/mixtral-8x7b-instruct-v01-q"
with open('API_creds.json') as f :
    creds = json.load(f)
    BAM_API_Key = creds["BAM_Key"]
    BAM_URL = creds["BAM_URL"]



def Prompt_Input(prompt, articleTitle, articleText) :
    input = f'''
    Input: Title: {articleTitle}

    Text: {articleText}
    Output:'''
    return prompt + input

def Prompt_Input_Single_Article_Summary(prompt, articleTitle, articleText) :
    input = f'''
    Title: {articleTitle}

    Text: {articleText}
    <|assistant|>'''
    return prompt + input

def Prompt_Input_Single_Bullet(prompt, articleTitle, articleText) :
    input = f'''
    Title: {articleTitle}

    Text: {articleText}
    Output: \n'''
    return prompt + input


#Returns the generated text
def Query_BAM_REST(prompt) :
    body = {'model_id': 'ibm/granite-13b-instruct-v2', 'input': prompt, 'parameters': {}}
    body['parameters']['decoding_method'] = 'greedy'
    body['parameters']['include_stop_sequence'] = True
    body['parameters']['stop_sequences'] = ['---']
    body['parameters']['max_new_tokens'] = 200

    headers = {'Authorization': f'Bearer {BAM_API_Key}'}
    return requests.post(BAM_URL, json=body, headers=headers).json()['results'][0]['generated_text']

#Returns the generated text
def Query_BAM(prompt, num_tokens) :
    client = Client(credentials=Credentials(api_key=BAM_API_Key, api_endpoint=BAM_URL))
    parameters = TextGenerationParameters(
        max_new_tokens=num_tokens,
        decoding_method=DecodingMethod.GREEDY,
        include_stop_sequence=False,
        stop_sequences=['---']
    )
    llm = LangChainInterface(
        model_id=model_id,
        client=client,
        parameters=parameters
    )
    response = llm.generate(prompts=[prompt])
    print(response.generations[0][0])
    return response.generations[0][0].text

def Query_WX(text) :
    my_credentials = { 
    "url"    : "https://us-south.ml.cloud.ibm.com", 
    "apikey" : "PUT API KEY HERE"
    }

    model_id    = 'ibm/granite-13b-instruct-v2'
    gen_params = {
        GenParams.MAX_NEW_TOKENS: 200
    }
    project_id  = "PUT PROJECT KEY HERE"
    space_id    = None
    verify      = False   
    gen_params_override = None
    model = Model( model_id, my_credentials, gen_params, project_id, space_id, verify )
    generated_response = model.generate( text, gen_params_override )
    return generated_response

def run_llm(df) :

    num_rows, row_len = df.shape
    prompt_text = prompt

    # #Intialize the dataframe to add the 5 extra columns
    # cols_to_add = ["Country", "ShortTerm_IRtrend", "LongTerm_IRtrend", "ConsumerSpending", "Production", "Employment", "Inflation", "Geopolitics", "NetSentiment"]
    # for i in range(len(cols_to_add)) :
    #     df.insert(row_len, cols_to_add[i], None)
    #     row_len += 1

    #Running LLM
    results = []
    for i in range(num_rows) :
        articleTitle = df.iloc[i]['Title']
        articleText = df.iloc[i]['Text']
        response = Query_BAM(Prompt_Input(prompt_text, articleTitle, articleText), 200)
        try:
            output_text = response.replace('---', '').replace(' ', '').replace('\n', '')
            #print(output_text)
            dct = json.loads(output_text)
            results.append(dct)
            update_row_with_dict(df, dct, i)
            get_net_sentiment(df, i)
        except:
            results.append({})
            print(f'Error reconverting output to dictionary on row {i}')


def do_single_llm(df, i) :
    #prompt_f = open("Prompt.txt")
    prompt_text = prompt
    articleTitle = df.iloc[i]['Title']
    articleText = df.iloc[i]['Text']
    response = Query_BAM(Prompt_Input(prompt_text, articleTitle, articleText), 200)
    try:
        #print(response.json()['results'])
        output_text = response.replace('---', '').replace('\n', '')
        dct = json.loads(output_text)
        update_row_with_dict(df, dct, i)
        get_net_sentiment(df, i)
    except Exception as e:
        print(f'Error retrieving output to dictionary on row {i}')
        #print(traceback.format_exc(e))

#Run summary for bullet point summary on single article (id i in dataframe df)
def single_article_summary(df, i) :
    prompt_text = single_article_summary_prompt
    articleTitle = df.iloc[i]['Title']
    articleText = df.iloc[i]['Text']
    output_text = Query_BAM(Prompt_Input_Single_Article_Summary(prompt_text, articleTitle, articleText), 300)
    try:
        #print(response.json()['results'])
        output_text = output_text.replace("$", "\$")
        df.loc[i, 'Multi-Point Summary'] = output_text
        return output_text
    except Exception as e:
        print(f'Error retrieving output to dictionary on row {i}')
        return ""
    

#Uses all of the headlines in the dataframe to come up with a set of categories, and associates each article with one
def get_categories(df) :
    prompt_text = categories_prompt
    num_rows, _ = df.shape
    headlines = ""
    for i in range(num_rows) :
        headlines = headlines + f"Article {i + 1}: {df.iloc[i]['Title']}\n\n"
    
    prompt = prompt_text + headlines + "Output: "
    return Query_BAM(prompt, 500)

#the full process for the bank exec dashboard/newsletter
def get_full_summary(df) :
    category_dictionary = {}
    num_rows, _ = df.shape
    prompt_text = single_bullet_prompt
    p_bar = st.progress(0.0, "Getting categories")

    try:
        response = get_categories(df).replace('---', '')
        #print(response)
        category_dictionary = json.loads(response)
    except Exception as e:
        print('Error retrieving category output to dictionary')
        p_bar.empty()
        return False
    
    #assign category to each article
    for key in category_dictionary.keys() :
        for article_id in category_dictionary[key] :
            df.loc[article_id - 1, "Category"] = key

    for i in range(num_rows) :
        p_bar.progress((i + 2)/(num_rows + 1), f"Getting summary for article {i + 1}")
        articleTitle = df.iloc[i]['Title']
        articleText = df.iloc[i]['Text']
        response = Query_BAM(Prompt_Input_Single_Bullet(prompt_text, articleTitle, articleText), 200)
        response = response.replace("---", "").replace("\n", "").replace(" $", " \$").replace("Summary: ", "").replace("  ", "")
        #print(response)
        df.loc[i, "Summary"] = response

    p_bar.empty()
    return True
