#!/usr/bin/env python3

from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv


def new_connection(collection):
    """
    Returns a connection to the mongo collection.
    """
    load_dotenv()
    host = getenv("HOST")
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    database = getenv("DATABASE")
    client = MongoClient('mongodb://'+username+':'+password+'@localhost:27017/')


    db = client[database][collection]
    return db
    
    
    
