# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: codedong
@mail:  vole_store@163.com
@time: 17-12-20 下午4:40
@file: cnBlog
"""

import requests
from lxml import etree
from util.fileDeal.genCsv import genCsv
from db.MongoDBHelp import MongoHelper
import datetime


class cnBlog:
    def __init__(self):
        self.mh = MongoHelper()
        self.mh.init_db("Cspider", "cnBlog")

    def get_data(self):
        resp = requests.get("http://www.cnblogs.com/pick/")

        # print(resp.text)
        self.parse_data(resp.text)

    def parse_data(self, html):
        tree = etree.HTML(html)
        blog_title = tree.xpath("//div[@class='post_item_body']/h3/a/text()")
        publish_date = tree.xpath("//div[@class='post_item_foot']")
        author = tree.xpath("//div[@class='post_item_foot']/a/text()")
        comment = tree.xpath("//span[@class='article_comment']/a/text()")
        view = tree.xpath("//span[@class='article_view']/a/text()")
        content = tree.xpath("//p[@class='post_item_summary']")
        diggnum = tree.xpath("//div[@class='diggit']/span/text()")
        print(author)
        print(comment)
        print(view)
        print(content)
        print(diggnum)
        self.save_data(blog_title, publish_date, author, comment, view, diggnum, content)

    def save_data(self, blog_title, publish_date, author, comment, view, diggnum, content):
        headers = ['blog_title', 'publish_date', 'author', 'comment', 'view', 'diggnum', 'content', 'date']
        cv = genCsv('../../data.csv', headers)
        # print(pro_shop_location, pro_shop_name, pro_price, pro_salecount)
        # print(len(pro_title), pro_title[0].xpath('string(.)').strip())
        for i, item in enumerate(blog_title):
            row = {"blog_title": blog_title[i].strip(), "publish_date": publish_date[i].xpath('string(.)').strip(),
                   "author": author[i],
                   "comment": comment[i].strip(), "view": view[i], "content": content[i].xpath('string(.)').strip(),
                   "diggnum": diggnum[i], "date": datetime.datetime.utcnow()}
            cv.write_data(row)
            # row["date"] = datetime.datetime.utcnow()
            self.mh.insert_data(row)
        cv.file_close()


if __name__ == '__main__':
    cb = cnBlog()
    cb.get_data()
