import time

import pymongo
from db.ISQLHelper import ISQLHelper
from config import DB_CONFIG


class MongoHelper(ISQLHelper):
    def __init__(self,):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)

    def init_db(self,db_name):
        #create_time = time.strftime('%Y/%m/%d', time.localtime(time.time()))

        self.db = self.client[db_name]
        self.collection = self.db['58_house']

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        if value:
            houseObj = dict(title=value['title'], update_info=value['update_info'], phone=value['phone'],total_Price=value['total_price'],
                           per_price=value['per_price'],
                           house_type =value['house_type'], area=value['area'],village_name=value['village_name'])
            self.collection.insert(houseObj)

    def delete(self, conditions=None):
        if conditions:
            self.collection.remove(conditions)
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.collection.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def select(self, count=None, conditions=None,page=None):
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None)
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}
        items = self.collection.find(conditions, limit=count).skip(int(page)).sort(
            [("time", pymongo.DESCENDING)])
        results = []
        for item in items:
            result = (item['title'], item['url'], item['category'],item['content'],item['img_path'],)
            results.append(result)
        return results
    def close_client(self):
        self.client.close()

    def count(self,condition=None):
        condition=dict(condition)
        return self.collection.find(condition).count()


if __name__ == '__main__':
    from db.MongoHelp import MongoHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    # # print  sqlhelper.select(None,{'types':u'1'})
    # items= sqlhelper.proxys.find({'types':0})
    # for item in items:
    # print item
    # # # print sqlhelper.select(None,{'types':u'0'})
    pass

