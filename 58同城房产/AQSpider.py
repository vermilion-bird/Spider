
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.proxy import ProxyType

from db.MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import config
import re
import time
from PIL import Image
from  io import BytesIO
import pytesseract
import random
class Crawl():
    def __init__(self):
        self.SqlH =SqlHelper()
        self.SqlH.init_db("AQhouse")
        self.totla_url_set=set()
        self.wait_use_url_set=set()
        self.start_url='http://anqing.58.com/ershoufang/29438496206005x.shtml?from=1-list-3&iuType=z_0&PGTID=0d300000-0000-0cfa-20ea-929be2f88bf7&ClickID=3&adtype=3'

        pass
    def crawlData(self,url):
        #设置phantomjs
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = (config.get_header())
        # 不载入图片，爬页面速度会快很多
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = random.choice(ips)
        # proxy.add_to_capabilities(desired_capabilities)
        # 打开带配置信息的phantomJS浏览器
        # driver = webdriver.PhantomJS(executable_path=phantomjs_driver,desired_capabilities=desired_capabilities)
        driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
        driver.start_session(desired_capabilities)
        # 隐式等待5秒，可以自己调节
        driver.implicitly_wait(5)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        driver.set_page_load_timeout(20)
        # 设置10秒脚本超时时间
        driver.set_script_timeout(20)
        #browser = webdriver.Chrome('/home/caidong/developProgram/selenium/chromedriver')
        driver.get(url)
        driver.implicitly_wait(1)
        driver.find_element_by_xpath('//div[@class="house-chat-phone"]').click()
        html = driver.page_source
        return html
    def parse(self,html):
        tree=etree.HTML(html)
        house_link=tree.xpath('//a/@href')
        for link in house_link:
            erlink=re.match("^http://anqing.58.com/ershoufang/.+",link)
            if erlink!=None and erlink.group(0) not in self.totla_url_set:
                self.wait_use_url_set.add(erlink.group(0))
                self.totla_url_set.add(erlink.group(0))
                print(erlink.group(0))
        print(house_link)
        title= tree.xpath('//div[@class="house-title"]/h1/text()')
        update_info = tree.xpath('//p[@class="house-update-info"]/span[@class="up"][1]/text()')
        phone = tree.xpath('//p[@class="phone-num"]/text()')
        total_price = tree.xpath('//p[@class="house-basic-item1"]/span[@class="price"]/text()')
        per_price = tree.xpath('//span[@class="unit"]/text()')
        house_type = tree.xpath('//p[@class="room"]/span[@class="main"]/text()')
        area = tree.xpath('//p[@class="area"]/span[@class="main"]/text()')
        village_name = tree.xpath('//span[@class="c_000 mr_10"]/text()')
        content = {"title":title[0].strip() ,"update_info":update_info[0].strip(),"phone":phone[0].strip(),"total_price":total_price[0].strip(),"per_price":per_price[0].strip().replace(" ",""),"house_type":house_type[0].strip(),"area":area[0].strip(),"village_name":village_name[0].strip()}
        print(content)
        return content

if __name__ == '__main__':
    crawl=Crawl()
    html = crawl.crawlData(crawl.start_url)
    content = crawl.parse(html)
    crawl.SqlH.insert(content)
    use_url_set=crawl.wait_use_url_set
    time.sleep(5)
    print(use_url_set)
    for url in use_url_set:
        if url!="":
            html = crawl.crawlData(url)
            content = crawl.parse(html)
            crawl.SqlH.insert(content)
        else:
            use_url_set=crawl.wait_use_url_set