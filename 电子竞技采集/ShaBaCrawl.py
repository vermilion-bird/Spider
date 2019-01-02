# encoding utf-8
import datetime
import time
import uuid

from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from LoggerHelp import Gblogger
from SQLHelp import SQLHelp, PanKou, GameInfo, Leagueinfo
from config import CONFIG, Stanard


class ShaBaCrawl:
    def __init__(self):
        self.sq = SQLHelp()
        self.source_site = CONFIG.get("Domain", 'https://www.letou321.com/cn/sport_esport')
        self.current_game_id = ''

    def get_ShaBa(self):
        try:
            Gblogger.info('启动沙巴')
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-gpu')
            if CONFIG.get('Browser_Invisible') == 'close':
                chrome_options.add_argument('--headless')
            client = webdriver.Chrome(chrome_options=chrome_options,
                                      executable_path=CONFIG.get('executable_path'))  # 如果没有把chromedriver
            # 加入到PATH中，就需要指明路径
            client.get(self.source_site)
            WebDriverWait(client, 1200).until((expected_conditions.presence_of_element_located((By.ID, "maincontent"))))
            client.switch_to.frame(client.find_element_by_id("maincontent"))
            WebDriverWait(client, 1200).until((expected_conditions.presence_of_element_located((By.ID, "sportsFrame"))))
            client.switch_to.frame(client.find_element_by_id("sportsFrame"))
            client.maximize_window()
            while True:
                self.batch = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

                try:
                    if client.find_element_by_id('maincontent'):
                        client.switch_to.frame(client.find_element_by_id("maincontent"))
                    if client.find_element_by_id('sportsFrame'):
                        client.switch_to.frame(client.find_element_by_id("sportsFrame"))
                except NoSuchElementException as e:
                    pass
                    # Gblogger.error(e)
                WebDriverWait(client, 1200).until(
                    (expected_conditions.presence_of_element_located(
                        (By.XPATH, '//div[@class="oddsTable hdpou-a phase2 sport43"]'))))

                content = client.page_source
                path = etree.HTML(content)
                self.first_line_headers = path.xpath('//div[@class="oddsTable hdpou-a phase2 sport43"][1]//div['
                                                     '@class="oddsTitleWrap"]//div[@class="oddsTitle"]//div[@class="odds '
                                                     'subtxt"]/text()')
                hdpous = path.xpath('//div[@class="oddsTable hdpou-a phase2 sport43"]')  # [-1]  # 直播和未开始  过滤滚球
                for p_i, pou in enumerate(hdpous, 1):
                    pou = etree.ElementTree(pou)
                    league_groups = pou.xpath('//div[@class="leagueGroup"]')
                    for l_i, league in enumerate(league_groups, 1):
                        league = etree.ElementTree(league)
                        name = league.xpath('string(//div[@class="leagueName"])')  # 比赛名
                        self.gName = name
                        if ":" in name:
                            name = name.split(':')[0]
                        elif "-" in name:
                            name = name.split('-')[0]
                        name = Stanard.get(name.strip(), name)
                        is_exist = self.sq.is_exist(Leagueinfo.LeagueId, Leagueinfo.kname == name,
                                                    Leagueinfo.SourceSite == self.source_site)
                        if not is_exist:
                            bet_id = str(uuid.uuid1())
                            self.sq.insert_one(Leagueinfo(kname=name, LeagueId=bet_id,
                                                          SourceSite=self.source_site))
                        else:
                            bet_id = is_exist
                        normal_s = league.xpath('//div[@class="matchArea"]')
                        for n_index, normal in enumerate(normal_s, 1):
                            normal = etree.ElementTree(normal)
                            # 每场比赛第一行信息
                            # multi_odds = normal.xpath('//div[contains(@class,"normal-a")] | //div[contains(@class,'
                            #                           '"normal-b")] | //div[contains(@class,'
                            #                           '"live-a")] | //div[contains(@class,'
                            #                           '"live-b")]')
                            multi_odds = normal.xpath('//div[@class="normal-a"] | //div[@class="normal-b"] | //div[@class'
                                                      '="live-a"] | //div[@class'
                                                      '="live-b"]')
                            for mul_index, multiodd in enumerate(multi_odds, 1):
                                multiodd = etree.ElementTree(multiodd)
                                self.parse_first_line(multiodd, bet_id)
                                # # 提取地图一数据
                                inners = client.find_elements_by_xpath(
                                    "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                        p_i) + ']//div[@class="leagueGroup"][' + str(
                                        l_i) + ']//div[@class="matchArea"][' + str(
                                        n_index) + ']//div[contains(@class,"moreBetTypeArea")]//div['
                                                   '@class="oneSet-c"]')
                                for inner in inners:
                                    html = inner.get_attribute("outerHTML")
                                    one_set = etree.HTML(html)
                                    self.parse_map_data(one_set)
                            #  找出地图标签
                            maps = client.find_elements_by_xpath(
                                "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                    p_i) + "]//div[@class='leagueGroup'][" + str(
                                    l_i) + "]//div[@class='matchArea'][" + str(
                                    n_index) + "]//li[@class='moreBetTypeNav-Item']")

                            #  地图一之后数据
                            for m_i, map in enumerate(maps, 1):
                                print("//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                    p_i) + "]//div[@class='leagueGroup'][" + str(
                                    l_i) + "]//div[@class='matchArea'][" + str(
                                    n_index) + "]//li[@class='moreBetTypeNav-Item'][" + str(m_i) + "]")
                                try:
                                    # time.sleep(2)
                                    # buttom =   client.find_element_by_xpath(
                                    #     "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                    #         p_i) + "]//div[@class='leagueGroup'][" + str(
                                    #         l_i) + "]//div[@class='matchArea'][" + str(
                                    #         n_index) + "]//li[@class='moreBetTypeNav-Item'][" + str(m_i) + "]")
                                    # client.execute_script("arguments[0].scrollIntoView();",
                                    #                       buttom)  # 拖动到可点击位置
                                    # buttom.click()

                                    client.find_element_by_xpath(
                                        "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                            p_i) + "]//div[@class='leagueGroup'][" + str(
                                            l_i) + "]//div[@class='matchArea'][" + str(
                                            n_index) + "]//li[@class='moreBetTypeNav-Item'][" + str(m_i) + "]").click()

                                    # client.find_element_by_xpath(
                                    #     "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                    #         p_i) + "]//div[@class='leagueGroup'][" + str(
                                    #         l_i) + "]//div[@class='matchArea'][" + str(
                                    #         n_index) + "]//li[@class='moreBetTypeNav-Item'][1]").click()
                                except WebDriverException as e:
                                    Gblogger.error(e)
                                    # continue
                                inners = client.find_elements_by_xpath(
                                    "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                        p_i) + ']//div[@class="leagueGroup"][' + str(
                                        l_i) + ']//div[@class="matchArea"][' + str(
                                        n_index) + ']//div[contains(@class,"moreBetTypeArea")]//div['
                                                   '@class="oneSet-c"]')

                                # inners = client.find_elements_by_xpath(
                                #     "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                #         p_i) + ']//div[@class="leagueGroup"][' + str(
                                #         l_i) + ']//div[@class="matchArea"][0]//div[contains(@class,'
                                #                '"moreBetTypeArea")]//div[@class="oneSet-c"]')
                                for inner in inners:
                                    html = inner.get_attribute("outerHTML")
                                    one_set = etree.HTML(html)
                                    self.parse_map_data(one_set)
                            try:
                                client.find_element_by_xpath(
                                    "//div[@class='oddsTable hdpou-a phase2 sport43'][" + str(
                                        p_i) + "]//div[@class='leagueGroup'][" + str(
                                        l_i) + "]//div[@class='matchArea'][" + str(
                                        n_index) + "]//li[@class='moreBetTypeNav-Item'][1]").click()
                            except Exception as e:
                                pass

                Gblogger.info(str(self.batch) + '采集结束')
                time.sleep(CONFIG.get("Shaba_interval", 100))
        except Exception as e:
            Gblogger.error(e)
            time.sleep(1)

    def parse_first_line(self, normal, bet_id):
        """
        解析比赛第一行数据
        :param normal:
        :param bet_id:
        :return:
        """
        team_one = normal.xpath('string(//div[@class="team"][1])')  # 队伍1
        team_two = normal.xpath('string(//div[@class="team"][2])')  # 队伍2
        #规范化
        team_one = Stanard.get(team_one,team_one)
        team_two = Stanard.get(team_two,team_two)


        if (not team_one) and (not team_two):
            return
        date_time = normal.xpath('string(//div[@class="time"])')
        print('date_)))))time', date_time)

        now = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)
        telve_hour = datetime.timedelta(hours=12)
        if 'LIVE' in date_time or 'IN-PLAY' in date_time:
            date_time_str = date_time.split(' ')[1]
            date_time = datetime.datetime.strptime(date_time_str, '%H:%M%p')
            if '12:' in date_time_str:
                if 'PM' in date_time_str:
                    date_time = date_time.replace(year=now.year, day=now.day, month=now.month)
                elif 'AM' in date_time_str:
                    date_time = date_time.replace(year=now.year, month=now.month, day=now.day, hour=0) + one_day
            else:
                if 'PM' in date_time_str:
                    date_time = date_time.replace(year=now.year, day=now.day, month=now.month) + telve_hour
                elif 'AM' in date_time_str:
                    date_time = date_time.replace(year=now.year, month=now.month, day=now.day) + one_day

        elif not date_time:
            print('date_)))))time_jiji', date_time)

            date_time = None
            # 滚球
            self.current_game_id = None
            return

        else:
            date_time_str = date_time
            date_time = datetime.datetime.strptime(date_time, '%m/%d %H:%M%p')
            if '12:' in date_time_str:
                if 'PM' in date_time_str:
                    date_time = date_time.replace(year=now.year)
                elif 'AM' in date_time_str:
                    date_time = date_time.replace(year=now.year, hour=0)
            else:
                if 'PM' in date_time_str:
                    date_time = date_time.replace(year=now.year) + telve_hour
                elif 'AM' in date_time_str:
                    date_time = date_time.replace(year=now.year) + one_day

        is_exist = self.sq.is_exist(GameInfo.gameId, GameInfo.teamName1 == team_one,
                                    GameInfo.teamName2 == team_two,
                                    GameInfo.gametime == date_time, GameInfo.SourceSite == self.source_site)
        if not is_exist and date_time:
            date_time = date_time.replace(second=0, microsecond=0)
            game_id = str(uuid.uuid1())
            self.sq.insert_one(GameInfo(teamName1=team_one, teamName2=team_two, gametime=date_time, gameId=game_id,
                                        LeagueId=bet_id, SpiderPiCi=self.batch,
                                        SourceSite=self.source_site, gName=self.gName, StartPiCi=self.batch))
            Gblogger.info('比赛 ' + str(team_one) + ' - ' + str(team_two))

        else:
            game_id = is_exist
            self.sq.update_data(GameInfo, self.batch, GameInfo.gameId == is_exist)

        self.current_game_id = game_id

        odds = normal.xpath('//div[@class="odds subtxt"]')
        for odd, header in zip(odds, self.first_line_headers):
            cols = etree.ElementTree(odd)
            pk_score1 = cols.xpath('string(//div[@class="betArea"][1]//span[1])')
            pk_percent1 = cols.xpath('string(//div[@class="betArea"][1]/div[@class="oddsBet"]/span)')
            pk_score2 = cols.xpath('string(//div[@class="betArea"][2]//span[1])')
            pk_percent2 = cols.xpath('string(//div[@class="betArea"][2]/div[@class="oddsBet"]/span)')
            if pk_percent1 or pk_percent2:
                name = Stanard.get(header, header)
                if '让' in header:
                    if pk_score1:
                        pk_score2 = pk_score1
                        pk_score1 = '-' + pk_score1
                    else:
                        tmp_pk_score2 = pk_score2
                        pk_score2 = '-' + pk_score2
                        pk_score1 = tmp_pk_score2
                pk_percent1 = str(round(float(pk_percent1) + 1, 2))
                pk_percent2 = str(round(float(pk_percent2) + 1, 2))
                self.sq.insert_one(PanKou(pk_Name=name, pk_score1=pk_score1, pk_score2=pk_score2,
                                          pk_percent1=pk_percent1, pk_percent2=pk_percent2,
                                          SourceSite=self.source_site, gameId=game_id,
                                          SpiderPiCi=self.batch))
                Gblogger.info('盘口 ' + str(name) + ' - ' + self.source_site)

    def parse_map_data(self, one_set):
        """
            解析函数
            :return:
            """
        if not self.current_game_id:
            return
        # try:
        header = one_set.xpath('string(//div[@class="betTypeHeader"])')
        titles = one_set.xpath('//div[@class="betTypeTitle"]//div[@class="betCol"]/text()')
        odds = one_set.xpath('//div[@class="betTypeContent"]//div[@class="betCol"]')
        for odd, title in zip(odds, titles):
            cols = etree.ElementTree(odd)
            pk_score1 = cols.xpath('string(//div[@class="betArea"][1]//span[1])')
            pk_percent1 = cols.xpath('string(//div[@class="betArea"][1]/div[@class="oddsBet"]/span)')
            pk_score2 = cols.xpath('string(//div[@class="betArea"][2]//span[1])')
            pk_percent2 = cols.xpath('string(//div[@class="betArea"][2]/div[@class="oddsBet"]/span)')
            if pk_percent1 or pk_percent2:
                name = Stanard.get(header + '-' + title, header + '-' + title)
                if '让' in title:
                    if pk_score1:
                        pk_score2 = pk_score1
                        pk_score1 = '-' + pk_score1
                    else:
                        tmp_pk_score2 = pk_score2
                        pk_score2 = '-' + pk_score2
                        pk_score1 = tmp_pk_score2
                    # print(pk_percent1,pk_percent2)
                    # if pk_percent1:
                    #     pk_percent2 = pk_percent1
                    #     pk_percent1 = '-' + pk_percent1
                    # else:
                    #     tmp_ercent2 = pk_percent2
                    #     pk_percent2 = '-' + pk_percent2
                    #     pk_percent1 = tmp_ercent2
                pk_percent1 = str(round(float(pk_percent1) + 1, 2))
                pk_percent2 = str(round(float(pk_percent2) + 1, 2))

                self.sq.insert_one(PanKou(pk_Name=name, pk_score1=pk_score1, pk_score2=pk_score2,
                                          pk_percent1=pk_percent1, pk_percent2=pk_percent2,
                                          SourceSite=self.source_site, gameId=self.current_game_id,
                                          SpiderPiCi=self.batch))
                Gblogger.info('盘口 ' + str(name) + ' - ' + self.source_site)


if __name__ == '__main__':
    ShaBaCrawl().get_ShaBa()
    # ShaBaCrawl().parse_first_line('')
    # ShaBaCrawl().parse_map_data('','')
    # print(datetime.datetime.strptime('17:00PM', '%H:%M%p'))
    # date_time = 'LIVE 03:00AM'
    # now = datetime.datetime.now()
    # date_time_str = date_time.split(' ')[1]
    # date_time = datetime.datetime.strptime(date_time_str, '%H:%M%p')
    # print(date_time)
    # end = date_time.replace(year=now.year, month=now.month, day=now.day)
    # end += datetime.timedelta(days=1)
    # print(end)
