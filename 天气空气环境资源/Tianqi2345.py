import json
import requests
import demjson
from pandas import DataFrame as df
def tainqi_get(month):
    print('http://tianqi.2345.com/t/wea_history/js/{}/58357_{}.js'.format(month,month))
    resp = requests.get('http://tianqi.2345.com/t/wea_history/js/{}/58357_{}.js'.format(month,month))
    response_text =resp.text
    print(response_text)
    response_text = response_text[16:-1]
    # resp_json = json.loads(response_text)
    resp_json = demjson.decode(response_text)
    return resp_json['tqInfo']

    # print(resp_json)

def main():
    datas = []
    for i in range(1,13):
        resp_list = tainqi_get('2018{}'.format(str(i).zfill(2)))
        datas.extend(resp_list)

    data = df(datas)
    data.to_csv('suzhou.csv',index=False)
    print(data)

if __name__ == '__main__':
    main()