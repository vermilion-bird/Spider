# coding:utf-8

# import sys
import datetime
import time
from util.Browser.Phantomjs import PhantomjsBrowser
from lxml import etree
from util.fileDeal.genCsv import genCsv
from db.MongoDBHelp import MongoHelper


class taobaoSearch:
    def __init__(self, keyword):
        self.browser = PhantomjsBrowser()  # Chrome()
        self.mh = MongoHelper()
        self.mh.init_db("Cspider", "taobao")
        self.s_keyword(keyword)
        self.imgUrl = 'taobao.png'
        # self.args = sys.argv

    def s_keyword(self, keyword):
        # self.browser.driver.set_window_size(1080, 800)
        self.browser.driver.get('https://www.taobao.com/')
        time.sleep(2)
        self.browser.driver.find_element_by_id('q').send_keys(keyword)
        self.browser.driver.find_element_by_xpath(
            '//div[@class="search-button"]/button[@class="btn-search tb-bg"]').click()
        # for i in range(1, 20):
        #     height = 125 * i
        #     self.browser.driver.execute_script('window.scrollTo(0, ' + str(height) + ')')
        #     time.sleep(1)
        self.parse_data(html=self.browser.driver.page_source, kw=keyword)
        self.browser.driver.save_screenshot('../../tmpImg/taobao.png')
        #self.imgUrl = keyword + '.png'
        self.browser.driver.close()
        #+print(self.browser.driver.page_source)

    def parse_data(self, html, kw):
        tree = etree.HTML(html)
        #print(html)
        pro_title = tree.xpath('//div[@class="m-itemlist"]//div[@class="row row-2 title"]')  # 标题
        pro_shop_name = tree.xpath('//div[@class="shop"]/a/span[2]/text()')
        pro_shop_location = tree.xpath('//div[@class="location"]/text()')
        pro_price = tree.xpath('//div[@class="row row-1 g-clearfix"]/div[@class="price g_price '
                               'g_price-highlight"]/strong/text()')
        pro_salecount = tree.xpath('//div[@class="row row-1 g-clearfix"]//div[@class="deal-cnt"]/text()')
        print(pro_title)
        self.save_data(pro_title, pro_shop_name, pro_shop_location, pro_price, pro_salecount, kw)

    def save_data(self, pro_title, pro_shop_name, pro_shop_location, pro_price, pro_salecount, keyword):
        headers = ['kw', 'pro_title', 'date', 'pro_shop_name', 'pro_shop_location', 'pro_price', 'pro_salecount']
        cv = genCsv('../../data.csv', headers)
        # print(pro_shop_location, pro_shop_name, pro_price, pro_salecount)
        # print(len(pro_title), pro_title[0].xpath('string(.)').strip())
        for i, item in enumerate(pro_title):
            row = {"kw": keyword, "pro_title": pro_title[i].xpath('string(.)').strip(),
                   "pro_shop_name": pro_shop_name[i],
                   "pro_shop_location": pro_shop_location[i], "pro_price": pro_price[i],
                   "pro_salecount": pro_salecount[i][:-3], "date": datetime.datetime.utcnow()}
            cv.write_data(row)
            #row["date"] = datetime.datetime.utcnow()
            self.mh.insert_data(row)
        cv.file_close()


if __name__ == '__main__':
    tb = taobaoSearch("芯片 ")
    # kw = str(tb.args[1])
    # kw = ''
    # tb.s_keyword()
