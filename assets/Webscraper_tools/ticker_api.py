import requests, json

def get_ticker_from_name(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()
    try :
        company_code = data['quotes'][0]['symbol']
        return company_code
    except:
        return False


#Comment out when testing

# company_name=input("Enter a company name: ")
# company=get_ticker_from_name(company_name)
# print(company)

# API_KEY, API_URL = "", ""

# with open('alpha_api.json') as f :
#     creds = json.load(f)
#     API_KEY = creds["key"]
#     API_URL = creds["url"]


# def get_ticker_from_name(name) :
#     url = API_URL % (name, API_KEY)
#     r = requests.get(url)
#     data = r.json()
#     print(data)

#     if len(data["bestMatches"]) > 0 :
#         for ticker_dict in data["bestMatches"] :
#             if ticker_dict["4. region"] == "United States" :
#                 return ticker_dict["1. symbol"]
#         #if no US based ticker found, return just the first one
#         return data["bestMatches"][0]["1. symbol"]
#     else :
#         return False



    
#print(get_ticker_from_name("Alibaba"))
