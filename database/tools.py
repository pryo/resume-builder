# this file read profile json file into mongodb
from pymongo import MongoClient
import pymongo
import time
import json
import configparser
from pathlib import Path
from util.struct import Map
class Parser:
    def __init__(self,conf_path):
        self.config = configparser.ConfigParser()
        try:
            res =self.config.read(conf_path)
            if res==[]:
                raise FileNotFoundError()
        except FileNotFoundError:
            print('Read conf file failed!')

        #self.config.read(Path("./conf/local.ini"))
        self.client = MongoClient(self.config['DEFAULT']['Host'], int(self.config['DEFAULT']['Port']))
        self.profile_db = self.client.profile


# json_path = os.path.join(path, "../resuem.json")
    def loadJson(self):
        json_path = Path("./"+self.config["DEFAULT"]["Json"]).resolve()
        json_file=  open(str(json_path))
        self.profile_json = json.load(json_file)

    def insert(self,json_items, target_collection,):
        if type(json_items) is dict:
            name = json_items['basics']['name']
            label=json_items['basics']['label']
            if target_collection.find_one({"basics.name":name,"basics.label": label}):
                return
            else:
                json_items['timestamp'] = time.time()
                target_collection.insert_one(json_items)

        else:

            for item in json_items:
                if not target_collection.find_one(item):
                    target_collection.insert_one(item)
# insert resume
    def insertResume(self):
        self.loadJson()
        resuem_colleciton = self.profile_db.resume
        self.profile_json['timestamp'] = time.time()
        resuem_colleciton.insert_one(self.profile_json)
        #self.insert(self.profile_json,resuem_colleciton)

    def insertSubcat(self,collection_name,json_name):
        cat_json = self.profile_json[json_name]
        collection = self.profile_db[collection_name]
        if type(cat_json) is dict:
            cat_json['timestamp'] = time.time()
            collection.insert_one(cat_json)
        else:
            for item in cat_json:
                if not collection.find_one(item):
                    collection.insert_one(item)
        #cat_json=self.profile_json[json_name]
        #self.insert(cat_json, collection)



class Getter:
    def __init__(self,conf_path):
        self.config = configparser.ConfigParser()
        try:
            res =self.config.read(conf_path)
            if res==[]:
                raise FileNotFoundError()
        except FileNotFoundError:
            print('Read conf file failed!')
        self.client = MongoClient(self.config['DEFAULT']['Host'], int(self.config['DEFAULT']['Port']))
    def getCollection(self,name):
        return self.client.profile[name]
    def getResume(self,name):
        #this func will get the latest resume in the database
        self.resume_dict=self.client.profile.resume.find_one\
            ({"basics.name":name},sort=[( 'timestamp', pymongo.DESCENDING )])
        return self.resume_dict
    def getWorks(self,query=None):
        cursor = self.client.profile.works.find(query,sort=[( 'endDate', pymongo.DESCENDING )])
        return [Map(work) for work in cursor]
    def getProjects(self,tags=["machine learning engineer","SDE"]):
        cursor = self.client.profile.projects.find({"tag":{"$in":tags}},sort=[( 'endDate', pymongo.DESCENDING )])
        return [Map(work) for work in cursor]
    def getEducation(self):
        cursor = self.client.profile.educations.find()
        return [Map(work) for work in cursor]
    def getSkills(self):
        cursor = self.client.profile.skills.find()
        return [Map(work) for work in cursor]
    def getAllTags(self):
        tags=set()
        cursor = self.client.profile.projects.find({})
        for p in cursor:
            tags.update(p['tag'])
        return list(tags)