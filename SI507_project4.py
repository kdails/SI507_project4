from bs4 import BeautifulSoup
import requests, json, csv
from db_setup import *

# setting up the caching ---- jackies code was hard, made simpler with less stuff from 506
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

BASEURL = "https://www.nps.gov"

#  create empty dictionary // set up cache from url
CACHEFILE = "nps_cache.json"

cache_diction = open_cache(CACHEFILE)

# get the data out of the dictionary; if not present, request to get & cache
nps_base_url = cache_diction.get(BASEURL)
if not nps_base_url:
    nps_base_url = requests.get(BASEURL).text
    cache_data(CACHEFILE,BASEURL,cache_diction,nps_base_url)

# create a BeautifulSoup object with the data
soup = BeautifulSoup(nps_base_url, "html.parser")

# get the text of the class that contains the list of states in the dropdown and add each state to the database if it doesn't already exist
dropdown =  soup.find('ul', class_='dropdown-menu SearchBar-keywordSearch')
#print(dropdown)
stated_tags = dropdown.find_all('li')
#print(stated_tags)
#print(type(stated_tags))
for item in stated_tags:
    # get the url to retrieve the state abbreviation and check if the state is already in the db
    url = item.a['href'] # all items with type tag href is a url
    chopped_url = url.split('/')
    state_exists = session.query(State.Abbr).filter(State.Abbr.like(chopped_url[2])).all()
    # if the state doesn't already exist, add it to the db
    if not state_exists:
        this_state = State(State=item.text,Abbr=chopped_url[2].upper(),URL='{}{}'.format(BASEURL,url))
        session.add(this_state)
session.commit()

# for each state retrieved from the States table, get the text from the url as stored in the db, cache it, and create a BeautifulSoup object
states = session.query(State.Id,State.URL).all()
for state in states:
    id = state[0]
    url = state[1]

    url_data = cache_diction.get(url)

    if not url_data:
        url_data = requests.get(url).text
        cache_data(CACHEFILE,url,cache_diction,url_data)
    soup = BeautifulSoup(url_data,'html.parser')
    parks_table = soup.find('ul', id='list_parks')
    parks_tagged = parks_table.find_all('li',class_='clearfix')
    for tag in parks_tagged:
        # check if the park currently exists in the db
        park_is_true = session.query(Park).filter(Park.Name == tag.h3.text).all()
        # if park exists, create a new rel; if not we must add it to the db
        # this code is like in discussion section- need break here to continue
        if park_is_true:
            rel_exists = session.query(StateParkAssociation).filter(StateParkAssociation.Park_Id == park_is_true[0].Id, StateParkAssociation.State_Id == id).all()
            if rel_exists:
                break
            else:
                new_rel = StateParkAssociation(State_Id=id,Park_Id=park_is_true[0].Id)
                session.add(new_rel)
                session.commit()
        else:
            new_park = Park(Name=tag.h3.text,Type=tag.h2.text,Descr=tag.p.text.strip('\n'),Location=tag.h4.text)
            session.add(new_park)
            session.commit()
            new_rel = StateParkAssociation(State_Id=id,Park_Id=new_park.Id)
            session.add(new_rel)
    session.commit()

# write the data to a csv file.... make db
with open('nps_parks.csv','w') as parks_file:
    parkwriter = csv.writer(parks_file)
    parkwriter.writerow(['Park Name','Park Type','Park Location Description','Park Description','Park States'])
    parks = session.query(Park).all()
    for park in parks:
        states = []
        rels = session.query(StateParkAssociation).filter(StateParkAssociation.Park_Id == park.Id).all()
        for rel in rels:
            this_state = session.query(State).filter(State.Id == rel.State_Id).first() # THIS_STATE CHANGE
            states.append(this_state.Abbr)
        parkwriter.writerow([park.Name,park.Type,park.Location,park.Descr,', '.join(states)])
