import re
import requests
from lxml import etree
from pandas import DataFrame

from Util.LoggerHelp import logger


class DianPing:
    def __init__(self, start_id, end_id):
        self.start = start_id
        self.end = end_id
        self.px_text = {}
        self.css_class_position = None
        self.num_encryp = {
            'kotej': '0',
            'komif': '2',
            'ko5mi': '3',
            'ko8ef': '4',
            'ko0g9': '5',
            'koefm': '6',
            'ko717': '7',
            'kod3h': '8',
            'koo2q': '9'
        }
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/68.0.3440.84 Safari/537.36',
                        }

    def get_page(self):
        for i in range(self.start, self.end):
            logger.info('http://www.dianping.com/shop/{}'.format(str(i)))
            resp = requests.get(
                'http://www.dianping.com/shop/{}'.format(str(i)), headers=self.headers)
            if resp.status_code != 404 :
                self.parse_page(resp.content.decode('utf-8'))
            else:
                logger.warn('指定ID店铺不存在' + str(i))

    def get_css_file(self, url):
        """
        :param mss_data:
        :param c_data:
        :return:
        """
        logger.info('http://'+url)
        resp = requests.get('http://' + url)
        css = resp.content.decode('utf-8')
        css_class = re.findall('}\w*?\[class\^=".."\]{.*?}', css)  #
        for c in css_class:
            label_name = c[1:c.index('[')]
            class_name = re.search('".."', c).group()
            svg_url = re.search('url\(//.*?\.svg', c)
            svg_url = svg_url.group()[6:]
            if class_name == '"rw"':
                self.rw_svg_to_df(svg_url)
        # css 类名,坐标 建立索引
        css_list = css.split(';}')
        css_lable = []
        px = []
        for item in css_list:
            re_item = item.replace('{background:', ' ')
            if re_item.endswith('px') and re_item and re_item.startswith('.'):
                re_item_strs = re_item[1:].split(' ')
                css_lable.append(re_item_strs[0])
                px.append((str(re_item_strs[1][1:-4]) + '_' + str(re_item_strs[2][1:-4])))
        df_css = DataFrame({
            'px': px
        }, index=css_lable)
        self.css_class_position = df_css

    def rw_svg_to_df(self, url):
        """
        :param url:
        :param label_name:
        :param class_start_word: 标签的class的开始两个字符
        :return:
        """
        resp = requests.get('http://' + url)
        row_num_px = {
            1: '13',
            2: '48',
            3: '85',
            4: '129',
            5: '163',
            6: '202',
            7: '246',
            8: '292'
        }
        resp = resp.content.decode('utf-8')
        text_lines = re.findall('>\w*?</textPath>', resp)
        list_text_px = []
        for row, line in enumerate(text_lines, 1):  # 行号对应的像素值
            line_text = line[1:-11]
            for col, word in enumerate(line_text):  # 列号对应的像素值
                list_text_px.append({
                    'value': word,
                    'px': str(col * 14) + '_' + str(row_num_px.get(row, 0))
                })
        df_text_px = DataFrame(list_text_px)
        df_text_px.set_index(["px"], inplace=True)
        self.px_text['rw'] = df_text_px

    def parse_address_word(self, class_vaule, start_key):
        """
        根据类名索引单词
        :param class_vaule:
        :return:
        """
        position = self.css_class_position.loc[class_vaule, 'px']
        try:
            word = self.px_text.get(start_key).loc[position, 'value']
        except Exception:
            word = ''
        return word

    def parse_page(self, html):
        code = re.search('s3plus.meituan.net.*?\.css', html).group(0)
        if code.endswith('.css'):
            self.get_css_file(code)
        et = etree.HTML(html)
        shop_name = et.xpath('//h1[@class="shop-name"]/text()')[0]
        logger.info('标题:'+ shop_name)
        adress_nodes = et.xpath('//span[@id="address"]/text()|//span[@id="address"]/*')
        address = '地址:'
        for address_word in adress_nodes:
            if not isinstance(address_word, str):
                # logger.info(address_word.tag)
                class_value = address_word.get('class')
                if class_value.startswith('rw'):
                    address += self.parse_address_word(class_value, 'rw')
                elif class_value.startswith('ko'):
                    address += self.num_encryp.get(class_value, '0')  # self.parse_address_word(class_value, 'ko')
            else:
                address += address_word
        logger.info(address)
        review_counts = et.xpath('//span[@id="reviewCount"]/text()|//span[@id="reviewCount"]/*')
        review = '评论:'
        for review_count in review_counts:
            if not isinstance(review_count, str):
                class_value = review_count.get('class')
                review += self.num_encryp.get(class_value)
            else:
                review += review_count
        logger.info(review)
        avg_prices = et.xpath('//span[@id="avgPriceTitle"]/text()|//span[@id="avgPriceTitle"]/*')
        avg_price = ''
        for prices in avg_prices:
            if not isinstance(prices, str):
                class_value = prices.get('class')
                avg_price += self.num_encryp.get(class_value)
            else:
                avg_price += prices
        logger.info(avg_price)

        comment_scores_spans = et.xpath('//span[@id="comment_score"]//span')
        for span in comment_scores_spans:
            span = etree.ElementTree(span)
            tastes = span.xpath('//*|//text()')
            taste_str = ''
            for item in tastes:
                if not isinstance(item, str):
                    if item.tag == 'd':
                        class_value = item.get('class')
                        taste_str += str(self.num_encryp.get(class_value))
                else:
                    taste_str += item
            logger.info(taste_str)
        tel_str = ''
        tels = et.xpath('//p[@class="expand-info tel"]//*|//p[@class="expand-info tel"]//text()')
        for item in tels:
            if not isinstance(item, str):
                if item.tag == 'd':
                    class_value = item.get('class')
                    tel_str += str(self.num_encryp.get(class_value))
            else:
                tel_str += item
        logger.info(tel_str)


if __name__ == '__main__':
    dp = DianPing(507574, 507579)
    dp.get_page()
