import datetime
import time
import uuid

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

from LoggerHelp import Gblogger
from config import CONFIG, Stanard
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from SQLHelp import SQLHelp, GameInfo, PanKou, Leagueinfo


class GbeSport:
    @staticmethod
    def get():
        try:
            Gblogger.info('启动GB')
            sq = SQLHelp()
            source_site = CONFIG.get("Domain", 'https://www.letou321.com/cn/gb_esport')
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            if CONFIG.get('Browser_Invisible') == 'close':
                chrome_options.add_argument('--headless')
            client = webdriver.Chrome(chrome_options=chrome_options,
                                      executable_path=CONFIG.get('executable_path'))
            # 加入到PATH中，就需要指明路径
            client.get(source_site)
            client.maximize_window()

            WebDriverWait(client, 1200).until(
                (expected_conditions.presence_of_element_located((By.ID, "thirdPartyGameFrame"))))
            client.switch_to.frame(client.find_element_by_id("thirdPartyGameFrame"))
            WebDriverWait(client, 1200).until(
                expected_conditions.element_to_be_clickable((By.XPATH, '//a[@class="click more '
                                                               'text-center clear"][1]')))
            while True:
                spider_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')#time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                index = 0
                try:
                    try:
                        if '电子竞技' not in client.find_element_by_xpath('//li[@class="title open-drop"]//a').text:
                            game_item = client.find_element_by_id('a_menu_sub_00111_1_-1')
                            client.execute_script("arguments[0].click();", game_item)  # 点击电子竞技
                    except Exception as e:
                        pass
                    tmp = ''
                    while True:
                        # 将滚动条移动到页面的顶部
                        # js = "var q=document.documentElement.scrollTop=0"
                        # client.execute_script(js)

                        WebDriverWait(client, 1200).until(
                            expected_conditions.presence_of_element_located(
                                (By.XPATH, '//a[@class="click more text-center clear"]')))
                        items = client.find_elements_by_xpath('//a[@class="click more text-center clear"]')
                        print('lendddd',len(items),index)
                        if index >= len(items):
                            # client.execute_script("window.scrollBy(0,3000)")

                            # slimScrollBar = client.find_element_by_xpath('//div[@class="slimScrollDiv"]//div[@class="slimScrollBar"]')
                            # ActionChains(client).drag_and_drop(source=slimScrollBar,target=slimScrollBar).perform()
                            # client.execute_script("arguments[0].scrollIntoView();", first_item[0])  # 拖动到可点击位置
                            # items.reverse()
                            # for i in items:
                            client.execute_script("arguments[0].scrollIntoView(false);", items[0])  # 拖动到可点击位置

                            break
                        name = client.find_element_by_xpath('//div[@id="div_listbetoption_1_4_template"]//div['
                                                            '@class="title-wrap clear"][' + str(
                            index + 1) + ']//h2').text
                        gnmae = name
                        if name:
                            name = name[name.index('[') + 1:name.index(']')]
                            name = Stanard.get(name.strip(), name)
                            tmp = name
                        if not tmp:
                            continue
                        is_exist = sq.is_exist(Leagueinfo.LeagueId, Leagueinfo.kname == tmp)

                        if not is_exist:
                            bet_id = str(uuid.uuid1())
                            sq.insert_one(Leagueinfo(kname=tmp, LeagueId=bet_id, SourceSite=source_site))
                        else:
                            bet_id = is_exist

                        date_time = client.find_element_by_xpath('//div[@id="div_listbetoption_1_4_template"]//div['
                                                                 '@class="content-wrap clear"][' + str(
                            index + 1) + ']//div[@class="time-wrap"]').text
                        if date_time:
                            now = datetime.datetime.now()
                            date_time_str = date_time
                            date_time = datetime.datetime.strptime(date_time, '%m/%d\n%H:%M %p')
                            date_time = date_time.replace(year=now.year)
                            if '12:' in date_time_str:
                                if 'PM' in date_time_str:
                                    date_time = date_time.replace(year=now.year)
                                elif 'AM' in date_time_str:
                                    date_time = date_time.replace(year=now.year, hour=0)
                            else:
                                if 'PM' in date_time_str:
                                    date_time = date_time + datetime.timedelta(hours=12)
                        else:
                            continue
                            # date_time =datetime.datetime.now()
                        team_one = client.find_element_by_xpath('//div[@id="div_listbetoption_1_4_template"]//div['
                                                                '@class="content-wrap clear"][' + str(
                            index + 1) + ']//div[@class="team-wrap"]//div[1]').text
                        team_two = client.find_element_by_xpath('//div[@id="div_listbetoption_1_4_template"]//div['
                                                                '@class="content-wrap clear"][' + str(
                            index + 1) + ']//div[@class="team-wrap"]//div[2]').text

                        # 规范化
                        team_one = Stanard.get(team_one, team_one)
                        team_two = Stanard.get(team_two, team_two)

                        is_exist = sq.is_exist(GameInfo.gameId, GameInfo.teamName1 == team_one,
                                               GameInfo.teamName2 == team_two, GameInfo.gametime == date_time,
                                               GameInfo.SourceSite == source_site)
                        if not is_exist:
                            gid = str(uuid.uuid1())
                            sq.insert_one(
                                GameInfo(teamName1=team_one, teamName2=team_two, gametime=date_time, gameId=gid,
                                         LeagueId=bet_id,SourceSite=source_site,SpiderPiCi=spider_time, gName=gnmae,StartPiCi=spider_time))
                        else:
                            gid = is_exist
                            sq.update_data(GameInfo, spider_time, GameInfo.gameId == is_exist)

                        Gblogger.info('比赛 ' + str(team_one) + ' - ' + str(team_two))
                        try:
                            client.execute_script("arguments[0].scrollIntoView();", items[index])  # 拖动到可点击位置
                        except StaleElementReferenceException as e:
                            Gblogger.error(e)
                            continue
                        client.execute_script("arguments[0].click();", items[index])  # 点击展开按钮
                        WebDriverWait(client, 1200).until(
                            (expected_conditions.presence_of_element_located(
                                (By.XPATH, '//section[@id="sec_nation_event"]//*'))))
                        html = client.find_element_by_id('sec_nation_event').get_attribute("outerHTML")
                        element = etree.HTML(html)
                        pre_match = element.xpath(
                            '//div[contains(@class,"pre-match-wrap")] |//div[contains(@class,"pre-match-wrap-h")]')
                        # 少一场比赛
                        for match in pre_match:
                            match = etree.ElementTree(match)
                            title = match.xpath('//h1/text()')[0]
                            if title:
                                if '正确比分' in title:
                                    continue
                                title = Stanard.get(title.strip(), title)
                            columns = match.xpath('div[contains(@class,"-column")]')
                            for col in columns:
                                ke_rang, team_one_score, team_two_score = '', '', ''
                                col = etree.ElementTree(col)
                                # 三列的逻辑
                                filter_thrid_col = col.xpath(
                                    '//div[@template="div_eventcontent_live_3-2_column_template"]')
                                # 删除队伍名
                                filter_team_name = col.xpath(
                                    '//ul[@template="ul_eventcontent_live_2-3_column_template"]')
                                # 需要过滤多余的客队的让分
                                filter_ke = col.xpath('//div[@template="div_eventcontent_live_2-1_1_column_template"]')

                                #  比赛获胜者 三项 多平局项
                                # template="ul_eventcontent_live_3-4_column_template"
                                filter_live_column = col.xpath(
                                    '//ul[@template="ul_eventcontent_live_3-4_column_template"]')
                                # 最后一行
                                filter_last_row = col.xpath(
                                    '//div[@template="div_eventcontent_live_2-2_column_template"]')

                                if filter_ke:
                                    # 客让
                                    filter_ke = etree.ElementTree(filter_ke[0])
                                    ke_rang = filter_ke.xpath('//li[1]//span[@class="word"]/text()')[0]
                                    team_one_score = filter_ke.xpath('//li[1]//a//del[@class="yellow"]/text()')[0]
                                    team_two_score = filter_ke.xpath('//li[2]//a//del[@class="yellow"]/text()')[0]


                                    pk_percent2 = ''
                                    if team_one_score or team_two_score:
                                        if '让' in title:
                                            if '+' in ke_rang:
                                                pk_percent2 = ke_rang.replace('+', '-')
                                            else:
                                                pk_percent2 = ke_rang.replace('-', '+')
                                        sq.insert_one(
                                            PanKou(pk_Name=title, pk_score1=ke_rang, pk_score2=pk_percent2,
                                                   pk_percent1=team_one_score, pk_percent2=team_two_score, gameId=gid,
                                                   SourceSite=source_site, SpiderPiCi=spider_time))

                                        Gblogger.info('盘口 ' + str(title) + ' - ' + source_site)

                                elif filter_team_name:
                                    filter_team_name = etree.ElementTree(filter_team_name[0])
                                    team_one_score = filter_team_name.xpath('//li[1]//del[@class="yellow"]/text()')[0]
                                    team_two_score = filter_team_name.xpath('//li[2]//del[@class="yellow"]/text()')[0]

                                    if team_one_score or team_two_score:
                                        sq.insert_one(
                                            PanKou(pk_Name=title, pk_score1='', pk_score2='',
                                                   pk_percent1=team_one_score, pk_percent2=team_two_score, gameId=gid,
                                                   SourceSite=source_site, SpiderPiCi=spider_time))
                                        Gblogger.info('盘口 ' + str(title) + ' - ' + source_site)

                                elif filter_thrid_col:
                                    filter_thrid_col = etree.ElementTree(filter_thrid_col[0])
                                    ke_rang = filter_thrid_col.xpath('string(//ul//li[1])')
                                    team_one_score = filter_thrid_col.xpath('string(//ul//li[2])')
                                    team_two_score = filter_thrid_col.xpath('string(//ul//li[3])')

                                    pk_percent2 = ''
                                    if team_one_score or team_two_score:
                                        if '让' in title:
                                            if '+' in ke_rang:
                                                pk_percent2 = ke_rang.replace('+', '-')
                                            else:
                                                pk_percent2 = ke_rang.replace('-', '+')
                                        sq.insert_one(
                                            PanKou(pk_Name=title, pk_score1=ke_rang, pk_score2=pk_percent2,
                                                   pk_percent1= team_one_score, pk_percent2= team_two_score, gameId=gid,
                                                   SourceSite=source_site, SpiderPiCi=spider_time))
                                        Gblogger.info('盘口 ' + str(title) + ' - ' + source_site)

                                elif filter_live_column:
                                    filter_live_column = etree.ElementTree(filter_live_column[0])
                                    team_one_score = filter_live_column.xpath('//li[1]//del[@class="yellow"]/text()')[0]
                                    team_two_score = filter_live_column.xpath('//li[3]//del[@class="yellow"]/text()')[0]

                                    if team_one_score or team_two_score:
                                        sq.insert_one(
                                            PanKou(pk_Name=title, pk_score1='', pk_score2='',
                                                   pk_percent1=team_one_score, pk_percent2=team_two_score, gameId=gid,
                                                   SourceSite=source_site, SpiderPiCi=spider_time))
                                        Gblogger.info('盘口 ' + str(title) + ' - ' + source_site)

                                elif filter_last_row:
                                    filter_last_row = etree.ElementTree(filter_last_row[0])
                                    team_one_score = filter_last_row.xpath('//li[1]//del[@class="yellow"]/text()')[0]
                                    team_two_score = filter_last_row.xpath('//li[2]//del[@class="yellow"]/text()')[0]

                                    if team_one_score or team_two_score:
                                        sq.insert_one(
                                            PanKou(pk_Name=title, pk_score1='', pk_score2='',
                                                   pk_percent1=team_one_score, pk_percent2=team_two_score, gameId=gid,
                                                   SourceSite=source_site, SpiderPiCi=spider_time))
                                        Gblogger.info('盘口 ' + str(title) + ' - ' + source_site)

                            #  回退到上一页
                        WebDriverWait(client, 120).until(expected_conditions.element_to_be_clickable(
                            (By.XPATH, '//a[@href="javascript:ListOption.ReviewHistory.Move(1);"]')))
                        clicks = client.find_element_by_xpath(
                            '//a[@href="javascript:ListOption.ReviewHistory.Move(1);"]')
                        client.execute_script("arguments[0].click();", clicks)

                        index += 1
                except Exception as e:
                    Gblogger.error(e)
                Gblogger.info(str(spider_time) + '采集结束')
                time.sleep(CONFIG.get('GB_interval',100))
        except Exception as e:
            Gblogger.error(e)
            time.sleep(10)


if __name__ == '__main__':
    GbeSport.get()
