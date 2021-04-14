import xml.etree.ElementTree as ET
import sys
import json
import urllib
import urllib.request
import pymongo
from pymongo import MongoClient
from pymongo import errors
import ssl
import argparse

#Initializing the MongoDB
client = pymongo.MongoClient("mongodb+srv://user:1234@cluster0.bnnrt.mongodb.net/sample_airbnb?retryWrites=true&w=majority",authSource='admin')
db = client.NASA
collection = db['S3VI']

#Command Line Help + Parser 
text = 'This program collects data from RSS feeds, inputs them into a mongo database, and displays the information. Please provide type as --type=[\'SSC\'|\'SSD\'|\'ALL\'] with \'ALL\' chosen by default. Search options may also be provided to parse through title and description by including --search=\"YOURQUERY\" '
parser = argparse.ArgumentParser(description=text)
parser.add_argument("-t", "--type", help = '"SSC" (SmallSat Conference), "SSD" (SmallSat Data) or "ALL". "ALL" is chosen by default')
parser.add_argument("-s", "--search", help = 'Search query to parse through title and description')
args = parser.parse_args()

#MongoDB Collection Checker
'''
try:
    col_dict = client.NASA.validate_collection(collection)
    print ('S3VI', "has", col_dict['nrecords'], "documents on it.\n")
except errors.OperationFailure as err:
    col_dict = None
    print ("PyMongo ERROR:", err, "\n")
'''

#Reset Collection to avoid creating duplicate results
response = client.NASA.drop_collection('S3VI')
if 'errmsg' in response:
    print ("drop_collection() ERROR:", response['errmsg'])
elif 'ns' in response:
        print ("the collection:", response['ns'], "is dropped.")


#Parsing the RSS sites and adding to the DB
for year in range(2017, 2020):
    req = urllib.request.Request(url='https://digitalcommons.usu.edu/smallsat/' + str(year) + '/all' + str(year) + '/recent-events.rss', method='GET')
    with urllib.request.urlopen(req) as f:
        tree = ET.parse(f)
        channels = tree.findall('channel')
        for channel in channels:
            items = channel.findall('item')
            for item in items:
                title = item.find('title').text
                date = item.find('pubDate').text
                author = item.find('author').text
                desc = item.find('description').text.strip()
                cleanlines = []
                for line in desc.splitlines():
                    cleanline = line.strip()[3:-4]
                    if len(cleanline):
                        cleanlines.append(cleanline)
                cleandesc = '\n'.join(cleanlines)
                doc = {
                    "title": title,
                    "author": author,
                    "date": date,
                    "description": cleandesc,
                    "data_type": "SSC"
                }
                collection.insert_one(doc)
    
    
#Dealing with json
with open('./data.json') as f:
  jsondata = json.load(f)
  for id in jsondata['data']:
    item = jsondata['data'][id]
    title = item['title']
    desc = item['description']
    date = item['lastUpdated']
    data_type = "SSD"
    jsonData = {
                "title": title,
                "author": author,
                "date": date,
                "description":desc,
                "data_type": "SSD"
            }
     #Checking for multiple authors for each object in json file        
    def getifexists(fields):
      arr = []
      for field in fields:
        if field in item.keys():
          arr = arr + item[field]
      return arr
    author = ', '.join(getifexists(['programDirectors', 'programManagers', 'principalInvestigators', 'coInvestigators']))
    collection.insert_one(jsonData)

#Printer Function
def printDoc(res):
    print('\n' + "Title: " + res['title'] + '\n')
    print("Date: " + res['date'] + '\n')
    print("Description: " + res['description'] + '\n')
    print("Author/Organization: " + res['author']+ '\n' + '\n')

# Command Line Argument Handling
if args.type == "SSC" or args.type == "SSD":
    print('\n'+ "Diplaying type as: % s" % args.type)
    if args.search:
        db['S3VI'].create_index( [ ("title", "text"), ("description", "text")] )
        results = db['S3VI'].find({"$and": [
            {"$text": { "$search": args.search}},
            {"data_type": args.type}
        ]}, {"_id": False})
        for res in results:
           printDoc(res)
    else: 
        for doc in collection.find({"data_type": args.type}):
            printDoc(doc)
else:
    print('\n' + "Diplaying type as: ALL")
    if args.search:
        db['S3VI'].create_index( [ ("title", "text"), ("description", "text")] )
        results = db['S3VI'].find({"$text": { "$search": args.search}})
        for res in results:
            printDoc(res)
    else:
        for doc in collection.find({}):   
            printDoc(doc)
