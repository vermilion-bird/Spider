#!/usr/bin/env python
# coding:utf-8
import random
import time

from lxml import etree
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# import config
# from MongoHelp import MongoHelper as SqlHelper
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ZHSpider:
    def __init__(self, start_page, end_page):
        self.black_page = 'https://www.zhihu.com/account/unhuman?type=unhuman&message=%E7%B3%BB%E7%BB%9F%E6%A3%80%E6' \
                          '%B5%8B%E5%88%B0%E6%82%A8%E7%9A%84%E5%B8%90%E5%8F%B7%E6%88%96IP%E5%AD%98%E5%9C%A8%E5%BC%82' \
                          '%E5%B8%B8%E6%B5%81%E9%87%8F%EF%BC%8C%E8%AF%B7%E8%BE%93%E5%85%A5%E4%BB%A5%E4%B8%8B%E5%AD%97' \
                          '%E7%AC%A6%E7%94%A8%E4%BA%8E%E7%A1%AE%E8%AE%A4%E8%BF%99%E4%BA%9B%E8%AF%B7%E6%B1%82%E4%B8%8D' \
                          '%E6%98%AF%E8%87%AA%E5%8A%A8%E7%A8%8B%E5%BA%8F%E5%8F%91%E5%87%BA%E7%9A%84 '
        self.start_page = start_page
        self.end_page = end_page
        self.toatal = self.start_page - self.end_page
        self.start_url = 'https://www.zhihu.com/people/zhang-jia-wei/followers?page=' + str(self.start_page)
        self.base_url = 'https://www.zhihu.com'
        self.SqlH = SqlHelper()
        self.SqlH.init_db('zhiHu', 'zhihu_all')
        proxy = {'address': '192.168.0.75:3128',
                 'usernmae': 'user15',
                 'password': 'iliketurtles'}

        capabilities = dict(DesiredCapabilities.CHROME)
        capabilities['proxy'] = {'proxyType': 'MANUAL',
                                 'httpProxy': proxy['address'],
                                 'ftpProxy': proxy['address'],
                                 'sslProxy': proxy['address'],
                                 'noProxy': '',
                                 'class': "org.openqa.selenium.Proxy",
                                 'autodetect': False}
        from selenium import webdriver
        # 进入浏览器设置
        options = webdriver.ChromeOptions()
        # 设置中文
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument("--proxy-server=http://192.168.0.75:3128")
        # 更换头部
        options.add_argument('Proxy-Authorization=Basic dXNlcjExOjEyMw==')

        options.add_argument('Proxy-Connection="keep-alive"')  # desired_capabilities=capabilities
        self.browser = webdriver.Chrome(executable_path='/home/caidong/chromedriver/chromedriver',
                                        chrome_options=options)
        # self.browser.get("chrome-extension://enhldmjbphoeibbpdhmjkchohnidgnah/options.html");

        # self.browser = webdriver.Chrome(executable_path='/home/caidong/developProgram/selenium/chromedriver')
        # self.browser = webdriver.PhantomJS()#service_args=service_args
        self.browser.get('http://2017.ip138.com/ic.asp')

        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys

        actions = ActionChains(self.browser)
        actions.send_keys("DSD")
        actions.send_keys(Keys.ENTER)
        actions.perform()
        # self.browser.find_element_by_id("url").sendKeys("http://www.baidu.com");
        # self.browser.find_element_by_id("username").sendKeys("user11");
        # self.browser.find_element_by_id("password").sendKeys("user12");
        # self.browser.find_element_by_class_name("credential-form-submit").click();
        # for char in 'user11':
        #     self.browser.setkeys(KE)

        # self.browser.find_element_by_xpath('//form').send_keys('dd')
        # self.browser.switch_to.alert().accept()

        time.sleep(1000)
        self.current = 1
        self.first_handle = None

        for c_page in range(self.start_page, self.end_page):
            try:
                self.crawlData(c_page)
            except:
                print("ERROR")
        self.browser.quit()

    def crawlData(self, c_page=1):
        url = 'https://www.zhihu.com/people/zhang-jia-wei/followers?page=' + str(c_page)
        self.browser.get(url)

        # 获取当前窗口的句柄
        self.first_handle = self.browser.current_window_handle

        self.browser.implicitly_wait(3)
        if self.browser.current_url == self.black_page:
            exit()
        if self.current == 1:
            time.sleep(5)
            self.logoin("13047811450", "1zzzzzhhhhh")  # random.choice(config.ACCOUNT), "123456")
            # self.logoin("13211521724","zzzzzhhhhh")
            self.current = self.current + 1
        time.sleep(2)
        c_page = self.browser.find_element_by_xpath(
            '//button[@class="Button PaginationButton PaginationButton--current Button--plain"]').text
        print('当前页:', c_page)
        # for curren_page in range(int(self.toatal)):
        #     self.browser.implicitly_wait(5)
        #     try:
        #         c_page = self.browser.find_element_by_xpath(
        #             '//button[@class="Button PaginationButton PaginationButton--current Button--plain"]').text
        #         print('当前页:', c_page)
        #         # 点击下一页
        #         # self.browser.find_element_by_xpath(
        #         #    '//Button PaginationButton PaginationButton-next Button--plain"]').click()
        #         # 点击上一页
        #         #self.browser.find_element_by_xpath(
        #         #    '//button[@class="Button PaginationButton PaginationButton-prev Button--plain"]').click()
        #         #self.browser.implicitly_wait(3)
        #     except:
        #         print("翻页出错")
        if self.start_page <= int(c_page) <= self.end_page:
            self.browser.implicitly_wait(5)
            intervalue = 2 + random.randrange(1, 4, 1)
            time.sleep(intervalue)
            self.parse_user_list(self.browser.page_source)




        else:
            exit()

    def parse_user_list(self, html):
        tree = etree.HTML(html)
        self.browser.execute_script('window.scrollTo(0, 100)')
        items = self.browser.find_elements_by_xpath('//div[@class="ContentItem-head"]//a[@class="UserLink-link"]')
        print("当前页用户数目", len(items))
        follower_list = tree.xpath('//div[@class="List-item"]')
        for index, item in enumerate(follower_list):
            # print(len(follower_list))
            print(str(index))
            ActionChains(self.browser).release()
            follower_info = etree.ElementTree(item)
            name = follower_info.xpath("//a[@class='UserLink-link']/text()")[0]  # 用户名
            home_page = follower_info.xpath("//a[@class='UserLink-link']/@href")[0]  # 主页
            follower_c = follower_info.xpath("//span[@class='ContentItem-statusItem']/text()")[2]  # 关注数
            print("链接", home_page)
            if self.SqlH.count({"user_home_url": home_page}) == 0:  # and int(follower_c[:-3].strip()) > 0
                print("新用户", name)
                # 不出现点击点问题
                # time.sleep(random.randrange(2))
                # self.browser.find_element_by_link_text(name).click()
                # cd_item = self.browser.find_elements_by_xpath('//div[@class="List-item"]//div[@class="ContentItem-image"]//a[@class="UserLink-link"]')
                # cd_item[index].click()
                # print('类比',len(cd_item))
                #
                # try:
                #     #self.browser.find_element_by_xpath('//div[@class="List-item"]['+str(index+1)+']/div[@class="ContentItem"]/div[@class="ContentItem-main"]/div[@class="ContentItem-head"]/h2[@class="ContentItem-title"]/div[@class="UserItem-title"]//a[@class="UserLink-link"]').click()
                #     #items[index].click()
                height = 125 * index
                self.browser.execute_script('window.scrollTo(0, ' + str(height) + ')')
                wait = WebDriverWait(self.browser, 20)
                #   超时异常
                try:
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="List-item"][' + str(
                        index + 1) + ']/div[@class="ContentItem"]/div[@class="ContentItem-main"]/div[@class="ContentItem-head"]/h2[@class="ContentItem-title"]/div[@class="UserItem-title"]//a[@class="UserLink-link"]')))  # //a[@class="UserLink-link"]
                except:
                    break
                ActionChains(self.browser).move_to_element(items[index]).click_and_hold().release().perform()
                print("点击了")
                #     time.sleep(3)
                # except Exception :
                #       print('点击错误')

                #     wait = WebDriverWait(self.browser, 10)
                #     element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ContentItem-head"]//a[@class="UserLink-link"]')))
                #     #while not items[index].is_displayed():
                #     #    time.sleep(1)
                #     self.browser.implicitly_wait(5)
                #     ActionChains(self.browser).move_to_element(items[index]).click().release().perform()
                #     time.sleep(5)
                #     print('点击正常')
                self.browser.implicitly_wait(1)
                handle_cnt = len(self.browser.window_handles) - 1
                # print('标签数',handle_cnt)
                self.browser.switch_to.window(self.browser.window_handles[handle_cnt])
                # print(self.browser.current_url)
                if self.browser.current_url == self.black_page:
                    time.sleep(10 * 60)
                self.browser.implicitly_wait(3)
                if handle_cnt > 0:
                    time.sleep(2)
                    if not self.browser.page_source.__contains__(
                            '<h1 class="ProfileLockStatus-title">该用户暂时被反作弊限制</h1>'):
                        try:
                            self.parse_special_column(self.browser.page_source, home_page)
                        except:
                            break;
                            print("")
                # 保留第一个标签页
                all_handles = self.browser.window_handles
                for window_handle in reversed(all_handles):
                    self.browser.switch_to.window(window_handle)
                    if window_handle != all_handles[0]:
                        self.browser.close()

            else:
                print("已存在,")
                continue

            time.sleep(random.randrange(2))

    def parse_special_column(self, html, url):
        tree = etree.HTML(html)
        follow = tree.xpath("//div[@class='NumberBoard-value']/text()")
        if follow:
            flowing = follow[0].strip()
            follower = follow[1].strip()
        else:
            flowing = 'none'
            follower = 'none'
        page_header = tree.xpath(
            "//div[@class='Card ProfileMain']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']/a/span/text()")
        answer = page_header[0]
        article = page_header[2]
        special_column = page_header[3]
        user_name = tree.xpath("//span[@class='ProfileHeader-name']/text()")[0]
        collecter = tree.xpath("//div[@class='Profile-sideColumnItemValue']/text()")
        # print("收藏数", collecter)
        if collecter:
            for item in collecter:

                if str(item).endswith("次收藏"):
                    save = item.strip()[:-3]
                else:
                    save = 0
        else:
            save = 0
        answer_list = []
        if int(answer) >= 4:
            try:
                self.browser.find_elements_by_xpath(
                    "//div[@class='Card ProfileMain']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']/a")[
                    0].click()
            except:
                self.browser.find_elements_by_xpath(
                    "//div[@class='Card ProfileMain']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']")[
                    0].click()
            height = 100
            # self.browser.find_element_by_link_text("回答")
            # self.browser.find_element_by_xpath("//div[@class='Card ProfileMain']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']/a[0]").click()
            for i in range(1, 4):
                self.browser.execute_script('window.scrollTo(0, ' + str(i * height) + ')')
            self.browser.implicitly_wait(5)
            time.sleep(2)
            tree = etree.HTML(self.browser.page_source)
            comment_list = tree.xpath('//div[@class="ContentItem-actions"]')
            if len(comment_list) >= 4:
                comment_list = comment_list[1:4]
            else:
                comment_list = comment_list[1:]
            for i, item in enumerate(comment_list):
                item = etree.ElementTree(item)
                answer_comment = item.xpath(
                    '//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]/text()')[
                    0]
                if str(answer_comment).startswith('添加'):
                    answer_comment = 0
                else:
                    answer_comment = str(answer_comment).strip()[:-3]
                answer_list.append(answer_comment)
        if len(answer_list) == 0:
            answer_list = "none"
        print("文章数", article, answer_list)
        if int(article) >= 4:
            try:
                self.browser.find_elements_by_xpath(
                    "//div[@class='Card ProfileMain']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']/a")[
                    2].click()
            except:
                self.browser.find_elements_by_xpath(
                    "//div[@class='PageHeader is-shown']//ul[@class='Tabs ProfileMain-tabs']/li[@class='Tabs-item']")[
                    2].click()
            height = 125
            for i in range(1, 4):
                self.browser.execute_script('window.scrollTo(0, ' + str(i * height) + ')')
            self.browser.implicitly_wait(5)
            time.sleep(2)
            article_list = self.parse_article(self.browser.page_source)
        else:
            article_list = 'none'
        obj = {"user_home_url": url,
               "user_name": user_name, "article_comment": article_list, "followers": follower, "flowing": flowing,
               "collect": save, "article": article,
               "answer": answer, "answer_comment": answer_list, "new": "true"}
        self.SqlH.insertZhiHu(obj)
        # self.SqlH.update({"user_home_url": self.user_home_url}, {
        #     "user_name":user_name,"article_comment":article_list,"followers": follower, "flowing": flowing,
        #                                    类                      "collect": save, "article": article,
        #                                                          "answer": answer, "answer_comment": answer_list,"new":"true"})
        print(user_name, "关注了", flowing, '收藏', str(save), '回答', answer, '文章', article, "跟随者", follower,
              special_column, '文章', article_list, '回答', answer_list)

    def parse_article(self, html):
        tree = etree.HTML(html)
        comment_list = tree.xpath('//div[@class="ContentItem-actions"]')
        if len(comment_list) >= 4:
            comment_list = comment_list[1:4]
        else:
            comment_list = comment_list[1:]
        article_list = []
        for item in comment_list:
            item = etree.ElementTree(item)
            answer_comment = item.xpath(
                '//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]/text()')[
                0]
            if str(answer_comment).startswith('添加'):
                answer_comment = 0
            else:
                answer_comment = str(answer_comment).strip()[:-3]
            print(answer_comment)
            article_list.append(answer_comment)

        if len(article_list) == 0:
            article_list = "none"
        print(article_list)
        return article_list

    def logoin(self, username, password):
        # print(self.browser.page_source)
        login = self.browser.find_elements_by_xpath("//div[@class='AppHeader-profile']/div/button")[0]
        login.click()
        self.browser.implicitly_wait(10)
        userinput = self.browser.find_element_by_xpath("//input[@name='username']")
        userinput.send_keys(username)
        pwdinput = self.browser.find_element_by_xpath("//input[@name='password']")
        pwdinput.send_keys(password)
        log_bt = self.browser.find_element_by_xpath(
            "//button[@class='Button SignFlow-submitButton Button--primary Button--blue']")
        log_bt.click()


if __name__ == '__main__':
    crawl = ZHSpider(49000, 50000)
    # 1502
