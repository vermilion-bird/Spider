import requests
from config import proxy_source

class getProxy:
    def __init__(self):
        self.source_url = proxy_source
        self.proxydic = {}

    def gainlist(self):
        resp = requests.get(self.source_url)
        self.proxydic = eval(resp.text)
        return eval(resp.text)
        #print(resp.text)


if __name__ == '__main__':
    gp = getProxy()
    print(gp.gainlist())
