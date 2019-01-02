import asyncio
import datetime
import pandas as pd
from collections import defaultdict
from urllib.parse import urlencode
import json
from pandas import DataFrame
from Util.RequestUtil import get_html
from config import ALL_CODE


class BaiduIndex:
    def __init__(self, startdate, enddate, city, key_word):
        self.start_date = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(enddate, '%Y-%m-%d')
        self.area = ALL_CODE.get(city, 0)
        self.key_words = key_word
        self.result = {keyword: defaultdict(list) for keyword in self.key_words}
        self._all_cate = ['all', 'pc', 'wise']
        self._headers = {
            'Cookie': ''
        }

    async def gen_date(self, start, end):
        """

        :param start:
        :param end:
        :return:
        """
        paramter = {
            'startDate': start,
            'endDate': end,
            'area': self.area,
            'word': self.key_words,

        }
        url = 'http://index.baidu.com/api/SearchApi/index?' + urlencode(paramter)
        html = await get_html(url, self._headers)
        datas = json.loads(html)
        uniqueid = datas['data']['uniqid']
        encrypt_datas = []
        for single_data in datas['data']['userIndexes']:
            encrypt_datas.append(single_data)
        return encrypt_datas, uniqueid

    async def gen_key(self, uniqueid):
        """

        :param uniqueid:
        :return:
        """
        url = 'http://index.baidu.com/Interface/api/ptbk?uniqid=%s' % uniqueid
        html = await get_html(url, header=self._headers)
        datas = json.loads(html)
        return datas['data']

    def trans_data(self, key, data):
        """

        :param key:
        :param data:
        :return:
        """
        a = key
        i = data
        n = {}
        s = []
        for o in range(len(a) // 2):
            n[a[o]] = a[len(a) // 2 + o]
        for r in range(len(data)):
            s.append(n[i[r]])
        return ''.join(s).split(',')

    def parse_save_data(self, data):
        """
        转化保存数据
        """
        data_dic_reshape = {}
        for cate in self._all_cate:
            data_dic_reshape[cate] = data[cate]['data']
        time_series = pd.date_range(start=self.start_date, end=self.end_date)
        data_df = DataFrame(data_dic_reshape, index=time_series)
        csv_name = './{}_指数_{}--{}.csv'.format(self.key_words, self.start_date.date(), self.end_date.date())
        data_df.to_csv(path_or_buf=csv_name, mode='w+')

    async def main(self):
        encrypt_datas, uniqid = await self.gen_date(self.start_date, self.end_date)
        key = await self.gen_key(uniqid)
        for encrypt_data in encrypt_datas:
            for kind in self._all_cate:
                encrypt_data[kind]['data'] = self.trans_data(key, encrypt_data[kind]['data'])
            self.parse_save_data(encrypt_data)


if __name__ == '__main__':
    baidu = BaiduIndex('2018-4-20', '2018-10-20', '', '王俊凯')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(baidu.main())
