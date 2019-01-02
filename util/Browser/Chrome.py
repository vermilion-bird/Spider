# coding:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile
import time
class Chrome:
    def __init__(self):
        manifest_json = """
        {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
        ],
        "background": {
        "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
        }
        """
        background_js = """
        var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
        scheme: "http",
        host: "192.168.0.75",
        port: parseInt(3128)
        },
        bypassList: ["foobar.com"]
        }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
        return {
        authCredentials: {
        username: "user12",
        password: "55"
        }
        };
        }

        chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
        );
        """
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        co = Options()
        co.add_argument("--start-maximized")
        co.add_extension(pluginfile)
        #co.add_argument("user-agent='Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1'")
        self.driver = webdriver.Chrome("/home/caidong/chromedriver/chromedriver", chrome_options=co)
        #driver.get("https://www.baidu.com")