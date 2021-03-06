import pandas as pd
from eda import clean_data
import pickle
import time
import requests
from bson.objectid import ObjectId
from fraud_model import MyModel

from pymongo import MongoClient
client = MongoClient()
db = client.fraud
pd.set_option("display.max_columns", 500)

def live_data(n=0):
    api_key = 'vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC'
    url = 'https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/'
    sequence_number = n
    response = requests.post(url, json={'api_key': api_key,
                                       'sequence_number': sequence_number})
    return response.json()


def store_data(n=0):
    for iter in range(n):
        data = live_data(iter)["data"][0]
        if db.live_records.find({"object_id": data["object_id"]}).count() == 0:
            db.live_records.insert(data)
            time.sleep(360)


def mongo_data():
    data = list(db.live_records.find())
    df = pd.DataFrame(data)
    return df

def segment(x):
    if x < 0.5:
        return "cleared"
    elif x < 0.65:
        return "low risk"
    elif x < 0.8:
        return "medium risk"
    else:
        return "high risk"

if __name__=="__main__":

    store_data(30)

