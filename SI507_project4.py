#setting up file structure here
from bs4 import BeautifulSoup
import requests, json, csv
from setup import *

# setting up the caching ---- jackies code was too hard, made simpler with less stuff from 506
def open_cache(CACHEFILE):
    try:
        with open(CACHEFILE,'r') as cache_file:
            cache_json = file.read()
            cache_diction = json.loads(cache_json)
    except:
        cache_diction = {}
    return cache_diction

def cache_data(CACHEFILE,url,cache_diction,new_data):
    with open(CACHEFILE,'w') as cache_file:
        cache_diction[url] = new_data
        cache_json = json.dumps(cache_diction) #read write --- both important here!
        cache_file.write(cache_json)
        
