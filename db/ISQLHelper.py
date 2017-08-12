# coding:utf-8


class ISQLHelper(object):
    params = {'ip': None, 'port': None, 'types': None, 'protocol': None, 'country': None, 'area': None}

    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, value=None):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def update(self, conditions=None, value=None):
        raise NotImplemented

    def select(self, count=None, conditions=None):
        raise NotImplemented

    def count(self,condition):
        raise  NotImplemented