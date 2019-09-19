#!/usr/bin/env python3

from scraper.settings import new_connection
from importlib import import_module
from scraper.sources import KNOWN_NEWS_SOURCES
import dateutil.parser as parser


def update_database(collection, headlines):
    if headlines is None:
        return
    from pymongo import InsertOne, ReplaceOne, UpdateOne

    # add new articles to db
    operations = []
    conn = new_connection(collection)
    for headline in headlines:

        diff = (parser.parse(headline["scraped_at"]) - parser.parse(headline["published_at"]).replace(tzinfo=None))
        db_object = {
            "link": headline["link"],
            "pub_date": headline["published_at"],
            "lifetime" : diff.total_seconds()//60,
            "title" : headline["title"]
        }
        if conn.count_documents({"link": headline["link"]}) == 0:
            operations.append(InsertOne(db_object))
        else:

            diff = (parser.parse(headline["scraped_at"]) - parser.parse(headline["published_at"]).replace(tzinfo=None))
            operations.append(UpdateOne(
                {"link": headline["link"]},
                {
                    "$set": {"lifetime":diff.total_seconds()//60}
                }
            ))
    conn.bulk_write(operations)
   

if __name__ == "__main__":
    # for key in KNOWN_NEWS_SOURCES:
    for key in ["The Hindu"]:
        src = KNOWN_NEWS_SOURCES[key]
        src["module"] = "scraper." + key.lower().replace(" ", "-")
        mod = import_module(src["module"])
        # import pdb;pdb.set_trace()
        try:
            headlines = mod.get_trending_headlines(src["home"])
            update_database(key, headlines)
            print("Done", key)
        except Exception as e:
            print("ERROR in", key)
            print("exception:"+str(e))
