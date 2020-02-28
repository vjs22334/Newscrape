#!/usr/bin/env python3

from scraper.settings import new_connection
from importlib import import_module
from scraper.sources import KNOWN_NEWS_SOURCES
import datetime as dt
import dateutil.parser as parser
from dateutil.tz import *
import pytz

tz = pytz.timezone('Asia/Kolkata')
local = tzlocal()


# def extract_headlines(headlines):
#     h=[]
#     import pdb; pdb.set_trace()
#     for x in headlines:
#         if parser.parse(x['published_at']) == (dt.datetime.today().replace(tzinfo=local).astimezone(tz) - dt.timedelta(1)).day:
#             h.append(x)
#     return h



def update_database(collection, headlines):

    if headlines is None or len(headlines) == 0:
        return
    from pymongo import UpdateOne,InsertOne
    operations = []
    conn = new_connection(collection)

    

    for headline in headlines:
        db_object = {
            "link": headline["link"],
            "published_time": headline["published_at"],
            "content": headline["content"],
            "title": headline["title"]
        }
        if conn.count_documents({"link": headline["link"]}) == 0:
            db_object["lifetime"] = 0
            operations.append(InsertOne(db_object))
            
        else:
            operations.append(UpdateOne(
                {"link": headline["link"]},
                {
                    "$set": {"content": headline["content"]}
                }
            ))
    conn.bulk_write(operations)


def to_go_on_next_page_or_not(collection, headlines):

    for x in headlines[:-1]:
        if parser.parse(x['published_at']) < dt.datetime.today().replace(tzinfo=local).astimezone(tz) - dt.timedelta(1):
            return False
    return True


if __name__ == "__main__":
    for key in KNOWN_NEWS_SOURCES:
        src = KNOWN_NEWS_SOURCES[key]
        src["module"] = "scraper." + key.lower().replace(" ", "-")
        src["module"] = import_module(src["module"])
    # for key in KNOWN_NEWS_SOURCES:
    # import pdb; pdb.set_trace()
    for key in ["The Hindu"]:
        print(key)
        src = KNOWN_NEWS_SOURCES[key]
        mod = src["module"]
        i=1
        while True:
            print(end=".")
            import sys
            sys.stdout.flush()
            try:
                if i == 1 and src["page1"] != "":
                    headlines = mod.get_chronological_headlines(src["page1"])
                else:
                    headlines = mod.get_chronological_headlines(src["pages"].format(i))
                if to_go_on_next_page_or_not(key, headlines):
                    i+=1    
                    update_database(key, headlines)
                else:
                    # update_database(key,extract_headlines(headlines))
                    update_database(key, headlines)
                    break
                print(" " + key + ": Scraping finished till", i - 1)
                
            except Exception as e:
                print("ERROR in", key,e)
                break
            
