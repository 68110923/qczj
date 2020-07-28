# -*- coding: utf-8 -*-
import scrapy
import logging
import time
import pymysql

from lxml import etree
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

from qczjbm.items import ZhiyuanGaodifenItem

XPATH = {
    '查询专业': ['xpath', '//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div[5]/div[2]/div[1]/div/div[1]/input'],
    '查询按钮': ['xpath', '//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div[5]/div[2]/div[1]/div/div[1]/button'],
    '全部按钮': ['xpath', '//*[@id="condition"]/li[1]/div[1]/span[1]'],

    '判断是否有数据': ['xpath', '//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[1]/table/tbody/tr[1]/td[1]'],
    '数据列表': ['xpath', '//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[1]/table/tbody'],
}


class ZhiyuanGaodifenSpider(scrapy.Spider):
    name = 'zhiyuan_gaodifen'
    allowed_domains = ['gkcx.eol.cn']
    start_urls = ['http://gkcx.eol.cn/']

    def parse(self, response):
        zhuanyemenlei=''
        banxueleixing=''
        self.driver = self.public_global_browser()
        self.get('https://gkcx.eol.cn/linespecialty')
        self.click(self.wait('xpath','//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div[3]/p'))
        self.click(self.wait('text','泉州市'))
        time.sleep(1)
        # for nianfen in ['2019','2018','2017']:
        for nianfen in ['2017','2016','2015']:
            for city in ['北京','天津','河北','河南','山东','山西','陕西','内蒙古','辽宁','吉林','黑龙江','上海','江苏',
                         '安徽','江西','湖北','湖南','重庆','四川','贵州','云南','广东','广西','福建','甘肃','宁夏','新疆',
                         '西藏','海南','浙江','青海']:
                # for banxueleixing in ['普通本科','独立学院','专科（高职)','中外合作办学','其他']:
                    # for zhuanyemenlei in ["哲学","经济学","法学","教育学","文学","历史学","理学","工学","农学","医学","管理学","艺术学","农林牧渔大类","资源环境与安全大类","能源动力与材料大类","土木建筑大类","水利大类","装备制造大类","生物与化工大类","轻工纺织大类","食品药品与粮食大类","交通运输大类","电子信息大类","医药卫生大类","财经商贸大类","旅游大类","文化艺术大类","新闻传播大类","教育与体育大类","公安与司法大类","公共管理与服务大类"]:
                self.get(f'https://gkcx.eol.cn/linespecialty?province={city}&luqutype=&schoolyear={nianfen}&schoolpc=&recomschprop=&schoolflag=&argschtype={banxueleixing}&zytype={zhuanyemenlei}')
                    # self.click(self.wait(XPATH['查询按钮'][0], XPATH['查询按钮'][1]), '查询')
                    # self.click(self.wait(XPATH['全部按钮'][0], XPATH['全部按钮'][1]), '全部')
                while True:

                    flig1 = True
                    try:
                        if self.read(self.wait(XPATH['判断是否有数据'][0], XPATH['判断是否有数据'][1],2)):
                            html=etree.HTML(self.driver.page_source)
                            for j in html.xpath('//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[1]/table/tbody/tr'):
                                school_name = j.xpath('./td[1]/text()')[0]
                                major_name = j.xpath('./td[2]/p/text()')[0]
                                admissions_address = j.xpath('./td[3]/text()')[0]
                                examinee_class = j.xpath('./td[4]/text()')[0]
                                admission_to_the_batch = j.xpath('./td[5]/text()')[0]
                                average_score = j.xpath('./td[6]/text()')[0]
                                lowest_mark = j.xpath('./td[7]/text()')[0]
                                yield ZhiyuanGaodifenItem(school_name=school_name, major_name=major_name,admissions_address=admissions_address,examinee_class=examinee_class,admission_to_the_batch=admission_to_the_batch,average_score=average_score,lowest_mark=lowest_mark,nianfen=nianfen,city=city,banxueleixing=banxueleixing,zhuanyemenlei=zhuanyemenlei)
                    except:
                        print('本页无数据')
                        flig1=False
                        break
                    finally:
                        if flig1:
                            next_ye=self.read(self.driver.find_elements_by_xpath('//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[2]/ul/li')[-3],attr='class',js=False)
                            if next_ye == 'none':
                                self.click(self.driver.find_elements_by_xpath('//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[2]/ul/li')[-2],'下一页')
                            elif next_ye == 'active':
                                print('没有下一页了')
                                break
                            else:
                                print(f'未知错误')
                                break


    def public_global_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"')
        options.add_argument('--disable-gpu')  # 规避bug
        # options.add_argument('--headless')    # 无头模式
        options.add_argument('--no-sandbox')  # 最高权限运行
        options.add_argument("--disable-javascript")  # 禁用JavaScript
        options.add_argument('--start-maximized')
        # options.add_argument("--proxy-server=http://36.248.129.75:9999")    # 设置ip
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 设置开发者模式启动，该模式下webdriver属性为正常值
        prefs = {'profile.default_content_setting_values': {'notifications': 2}}
        options.add_experimental_option('prefs', prefs)  # 禁用浏览器弹窗
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Network.enable", {})
        script = '''Object.defineProperty(navigator, 'webdriver', {get: () => undefined})'''
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
        driver.implicitly_wait(0.1)
        driver.set_page_load_timeout(20)  # 全局请求页面超时时间
        driver.set_script_timeout(20)  # 全局请求页面js加载超时时间
        return driver

    def end(self):
        self.driver.close()

    # 封装方法
    def wait(self, key, value, time_out=20, error='元素加载超时'):
        try:
            selector = {
                'id': By.ID,
                'xpath': By.XPATH,
                'text': By.LINK_TEXT,
                'name': By.NAME,
                'css': By.CSS_SELECTOR,
                'tag': By.TAG_NAME,
            }
            return WebDriverWait(self.driver, time_out, 0.3).until(
                EC.element_to_be_clickable((selector[key], value)))
        except Exception as e:
            print(f'等待>{key}=\'{value}\'  {error},{e}')
            raise e

    def click(self, element, name='目标元素', text=None, async_script=False, js=True):
        try:
            if not text or text in element.text:  # 判断条件成立可以进行写入操作
                if js and async_script:  # 判断条件成立使用异步JS进行写入
                    self.driver.execute_async_script("arguments[0].click();", element)
                elif js:
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    element.click()
                print(f'点击：{text or name}')
            else:
                print(f'点击：目标元素中不存在text：{text}')
        except Ellipsis as e:
            print(f'点击：{text or name}    {e}')

    def write(self, element, value, name=None, attr='value', js=True):
        try:
            if js:
                self.driver.execute_script(f"arguments[0].{attr}='{value}';", element)
            else:
                element.send_keys(value)
            print(f'填写：{name or ""}:{value}')
        except Ellipsis as e:
            print(f'填写：{name or ""}:{value}   {e}')

    def read(self, element, name=None, attr='textContent', js=True):
        try:
            if js:
                temp = self.driver.execute_script(f"return arguments[0].{attr};", element)
            else:
                temp = element.get_attribute(attr)
            print(f'读取：{name or attr}:{temp or ""}')
            return temp
        except Exception as e:
            print(f'读取：{name or attr}   {e}')
    def iframe(self, iframe=None, out_time=20):
        try:
            if iframe == '上一层':
                self.driver.switch_to.parent_frame()
            elif isinstance(iframe, int):
                iframe = self.driver.find_elements_by_tag_name('iframe')[iframe]
                WebDriverWait(self.driver, out_time, 0.5).until(EC.frame_to_be_available_and_switch_to_it(iframe))
            elif iframe:
                WebDriverWait(self.driver, out_time, 0.5).until(EC.frame_to_be_available_and_switch_to_it(iframe))
            else:
                self.driver.switch_to.default_content()
            print(f'切换iframe：{iframe or "default"}')
        except Exception as e:
            print(f'切换iframe：{iframe or "default"}')

    def windows(self, tab):
        try:
            if isinstance(tab, int):
                self.driver.switch_to.window(self.driver.window_handles[tab])
                print(f'切换windows：{tab} 的窗口')
            elif isinstance(tab, str):
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    if tab in self.driver.title:
                        print(f'切换windows：{tab} 的窗口')
                        break
        except Exception as e:
            print(f'切换windows：{tab} 的窗口')

    def get(self, url):
        try:
            self.driver.get(url)
            print(f'请求：{url}')
        except:
            self.driver.execute_script('window.stop()')
            print(f'请求：超时被阻塞:{url}')

    def get_new_window(self, url, tab=None):
        if not tab:
            tab = -1
        self.driver.execute_script(f'window.open("{url}")')
        print(f'请求：{url}')
        self.windows(tab)

    def move(self, element, name=None):
        try:
            ActionChains(self.driver).move_to_element(element).perform()
            print(f'移动鼠标：{name}')
        except Exception as e:
            print(f'移动鼠标：{name}')

    # 插件
    def plugin_write_down(self, element, value, down_number=1):
        # 向element写入数据 并 按下键点Enter
        self.write(element, value)
        if down_number > 0:
            for i in range(down_number):
                element.send_keys(Keys.DOWN)
        element.send_keys(Keys.ENTER)

    def plugin_read_config(self, file, select):
        temp = {}
        conf = ConfigParser()
        conf.read(file, encoding='utf-8')
        for k, j in conf.items(select):
            temp.update({k: j})
        return temp
