import pymongo
from config import *


class DataOutput(object):

    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_Host, MONGO_Port)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[KEYWORD]

    def save_mongo(self, data):
        self.collection.insert(data)

    def data_size(self):
        return self.collection.find().count()