                                                                            # !/usr/bin/python
                                                                            # -*- coding: utf-8 -*-

import base64
import time
import random

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from util.ProxyService.getProxy import getProxy


class PhantomjsBrowser():
    def __init__(self):
        # gp = getProxy().gainlist()
        # proxy = random.choice(gp)
        service_args = [
            '--ignore-ssl-errors=true',
            #'--proxy='+proxy["ip"]+':'+str(random.randint(3128,3140)),
            '--proxy=127.0.0.1:1080',
            #'--proxy=192.168.0.75:3129',
            '--proxy-type=http',
        ]
        authentication_token = "Basic " + base64.b64encode(b'user11:123').decode('utf-8')
        #print(authentication_token)
        capa = dict(DesiredCapabilities.PHANTOMJS)
        #capa['phantomjs.page.customHeaders.Proxy-Authorization'] = authentication_token
        # capa["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
        capa["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "
        )

        self.driver = webdriver.PhantomJS(desired_capabilities=capa)#service_args=service_args)
        # for key, v in capa.items():
        #     print('S', '%s: %s' % (key, v))
        #agent = self.driver.execute_script("return navigator.userAgent")
        self.driver.maximize_window()  # 设置最大窗体, 淘宝出现加载部分
        #print('ua', agent)
        # driver = webdriver.PhantomJS(service_args=service_args)
        # driver = webdriver.Firefox()  # Optional argument, if not specified will search path.
        # driver.get('http://1212.ip138.com/ic.asp');
        # driver.implicitly_wait(10)
        # print(driver.page_source)
        # # time.sleep(5) # Let the user actually see something!
        # search_box = driver.find_element_by_name('q')
        # search_box.send_keys('ChromeDriver')
        # search_box.submit()
        # self.driver.quit()
        # time.sleep(5)  # Let the user actually see something!
