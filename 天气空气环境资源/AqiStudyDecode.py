#/bin/sh
import json
import os
import requests
from pandas import DataFrame as df


cmd= "node vm.js %s %s %s %s" % ("getParam", "GETDAYDATA", '西安', '201908')
print(cmd)
format_data = os.popen(cmd).read().strip()
print('format_data',format_data)
resp =requests.post('https://www.aqistudy.cn/historydata/api/historyapi.php',data={"hd":format_data})
print(resp.text)
decode_cmd = "node vm.js %s %s" %("decodeData",resp.text)
res_data = os.popen(decode_cmd).read().strip()
print(df(json.loads(res_data)['result']['data']['items']).set_index('time_point'))