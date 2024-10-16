#Helper Functions
def remove_formatting(str) :
    return ''.join(s for s in str if ord(s)>31 and ord(s)<126).replace("   ", "").replace("$", "\$")

def update_row_with_dict(df,d,idx):
    keys = d.keys()
    for i in range(len(keys)) :
        df.loc[idx,list(keys)[i]] = d[list(keys)[i]]

# Getting net sentiment score of a single row i
def get_net_sentiment(df, i) :
    sentiment_to_int = {"Decrease": -1, "No Change": 0, "Increase": 1,}
    sent_headers = ["Interest Rate", "Consumer Spending", "Production", "Employment", "Inflation"]
    net_sentiment = 0
    for header in sent_headers :
        multiplier = -1 if header == "Inflation" else 1
        if df.iloc[i][header] in sentiment_to_int.keys() :
            net_sentiment += sentiment_to_int[df.iloc[i][header]] * multiplier
    df.loc[i, 'NetSentiment'] = net_sentiment