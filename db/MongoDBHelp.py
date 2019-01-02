import pymongo
from config import DB_CONFIG
import time


class MongoHelper():
    def __init__(self, ):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)

    def init_db(self, db_name, col_name):
        #create_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))+str(col_name)
        self.db = self.client[db_name]
        self.collection = self.db[col_name]

    def insert_data(self, value=None):
        if value:
            self.collection.insert(value)

    def select(self, count=1, conditions=None, page=1):
        if count:
            count = int(count)
        else:
            count = 0
        # if conditions:
        #     conditions = dict(conditions)
        #     conditions_name = ['types', 'protocol']
        #     for condition_name in conditions_name:
        #         value = conditions.get(condition_name, None)
        #         if value:
        #             conditions[condition_name] = int(value)
        # else:
        #     conditions = {}
        # items = self.collection.find(conditions,{'_id':0}, limit=count).skip(int(page)).sort(
        items = self.collection.find(conditions, {'_id': 0}, limit=count).skip(int(page)).sort(
            [("date", pymongo.DESCENDING)])
        results = []
        for item in items:
            #     result = (item['title'], item['url'], item['category'],item['content'],item['img_path'],)
            results.append(item)
        return results

    def count(self, condition= None):
        condition = dict(condition)
        return self.collection.find(condition).count()



