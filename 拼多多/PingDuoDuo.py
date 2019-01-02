import asyncio
from Util.RequestUtil import get_html
from lxml import etree
import pandas as pd


async def get_page(start_mall_id, end_mall_id):
    """

    :param start_mall_id:
    :param end_mall_id:
    :return:
    """
    for mall_id in range(start_mall_id, end_mall_id):
        resp = await get_html('http://yangkeduo.com/mall_page.html?mall_id={}'.format(str(mall_id)))
        await parse_page(resp, mall_id)


async def parse_page(html, mall_id):
    """
    :param html:
    :param mall_id:
    :return:
    """
    et = etree.HTML(html)
    goods_list = et.xpath('//div[@class="double-grid-one-v3 "]')
    goods_parsed_list = []

    for item in goods_list:
        item = etree.ElementTree(item)
        goods_name = item.xpath('//p[@class="goods-name"]/text()')
        goods_name = goods_name[0] if goods_name else ''
        sale_price = item.xpath('//p[@class="sale-price"]/text()')
        sale_price = sale_price[0] if sale_price else ''
        sold_quantity = item.xpath('//p[@class="sold-quantity"]/text()')
        sold_quantity = sold_quantity[0] if sold_quantity else ''
        goods_parsed_list.append({
            "goods_name": goods_name,
            "sale_price": sale_price,
            "sold_quantity": sold_quantity,
            "mall_id": mall_id
        })
    if goods_parsed_list:
        await save_data(goods_parsed_list)


async def save_data(goods_parsed_list):
    """

    :param goods_parsed_list:
    :return:
    """
    goods_df = pd.DataFrame(goods_parsed_list)
    goods_df.to_csv(path_or_buf='./拼多多.csv', mode='a+',)


loop = asyncio.get_event_loop()
loop.run_until_complete(get_page(1090493, 1090500))
