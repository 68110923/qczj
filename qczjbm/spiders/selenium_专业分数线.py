import logging
import time

from lxml import etree
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

XPATH = {
    '查询专业': ['xpath','//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div[5]/div[2]/div[1]/div/div[1]/input'],
    '查询按钮': ['xpath','//*[@id="root"]/div/div[1]/div/div/div/div/div[2]/div[5]/div[2]/div[1]/div/div[1]/button'],
    '全部按钮': ['xpath','//*[@id="condition"]/li[1]/div[1]/span[1]'],

    '判断是否有数据': ['xpath','//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[1]/table/tbody/tr[1]/td[1]'],
    '数据列表': ['xpath','//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[1]/table/tbody'],
}


class Tools:
    def __init__(self):
        self.log = self.public_global_log()
        self.driver = self.public_global_browser()

    def public_global_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"')
        options.add_argument('--disable-gpu')  # 规避bug
        # options.add_argument('--headless')    # 无头模式
        options.add_argument('--no-sandbox')  # 最高权限运行
        options.add_argument("--disable-javascript")  # 禁用JavaScript
        options.add_argument('--start-maximized')
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
        self.log.info('初始化：全局浏览器完成')
        return driver

    def public_global_log(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(funcName)s -> %(message)s')
        return logging

    def end(self):
        self.driver.close()
        self.log.warning('程序终止')

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
            self.log.error(f'等待>{key}=\'{value}\'  {error}')

    def click(self, element, name='目标元素', text=None, async_script=False, js=True):
        try:
            if not text or text in element.text:  # 判断条件成立可以进行写入操作
                if js and async_script:  # 判断条件成立使用异步JS进行写入
                    self.driver.execute_async_script("arguments[0].click();", element)
                elif js:
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    element.click()
                self.log.info(f'点击：{text or name}')
            else:
                self.log.warning(f'点击：目标元素中不存在text：{text}')
        except Ellipsis as e:
            self.log.error(f'点击：{text or name}    {e}')

    def write(self, element, value, name=None, attr='value', js=True):
        try:
            if js:
                self.driver.execute_script(f"arguments[0].{attr}='{value}';", element)
            else:
                element.send_keys(value)
            self.log.info(f'填写：{name or ""}:{value}')
        except Ellipsis as e:
            self.log.error(f'填写：{name or ""}:{value}   {e}')

    def read(self, element, name=None, attr='textContent', js=True):
        try:
            if js:
                temp = self.driver.execute_script(f"return arguments[0].{attr};", element)
            else:
                temp = element.get_attribute(attr)
            self.log.info(f'读取：{name or attr}:{temp or ""}')
            return temp
        except Exception as e:
            self.log.info(f'读取：{name or attr}        {e}')

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
            self.log.info(f'切换iframe：{iframe or "default"}')
        except Exception as e:
            self.log.error(f'切换iframe：{iframe or "default"}')

    def windows(self, tab):
        try:
            if isinstance(tab, int):
                self.driver.switch_to.window(self.driver.window_handles[tab])
                self.log.info(f'切换windows：{tab} 的窗口')
            elif isinstance(tab, str):
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    if tab in self.driver.title:
                        self.log.info(f'切换windows：{tab} 的窗口')
                        break
        except Exception as e:
            self.log.error(f'切换windows：{tab} 的窗口')

    def get(self, url):
        try:
            self.driver.get(url)
            self.log.info(f'请求：{url}')
        except:
            self.driver.execute_script('window.stop()')
            self.log.warning(f'请求：超时被阻塞:{url}')

    def get_new_window(self, url, tab=None):
        if not tab:
            tab = -1
        self.driver.execute_script(f'window.open("{url}")')
        self.log.info(f'请求：{url}')
        self.windows(tab)

    def move(self, element, name=None):
        try:
            ActionChains(self.driver).move_to_element(element).perform()
            self.log.info(f'移动鼠标：{name}')
        except Exception as e:
            self.log.error(f'移动鼠标：{name}')

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


class Crawler(Tools):
    def get_specialty(self):
        import pymysql
        specialty_ls=[]
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '000578',
            'database': 'blog',
            'charset': 'utf8',
        }
        conn = pymysql.connect(**dbparams)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM specialty;')
        specialty=cursor.fetchone()
        while specialty:
            specialty_ls.append(specialty)
            specialty = cursor.fetchone()
        cursor.close()
        conn.close()
        return specialty_ls
    def professional_score_line(self):
        self.get('https://gkcx.eol.cn/linespecialty?luqutype=&province=&schoolpc=&schoolyear=2019&recomschprop=&schoolflag=&argschtype=&zytype=')
        self.click(self.wait(XPATH['查询按钮'][0],XPATH['查询按钮'][1]),'查询')
        self.click(self.wait(XPATH['全部按钮'][0],XPATH['全部按钮'][1]),'全部')
        if self.read(self.wait(XPATH['判断是否有数据'][0],XPATH['判断是否有数据'][1])):
            html=etree.HTML(self.driver.page_source)
            for j in html.xpath('//*[@id="root"]/div/div[1]/div/div/div/div/div[3]/div[1]/div/div[1]/table/tbody/tr'):
                t1=j.xpath('./td[1]/text()')[0]
                t2=j.xpath('./td[2]/p/text()')[0]
                t3=j.xpath('./td[3]/text()')[0]
                t4=j.xpath('./td[4]/text()')[0]
                t5=j.xpath('./td[5]/text()')[0]
                t6=j.xpath('./td[6]/text()')[0]
                t7=j.xpath('./td[7]/text()')[0]
                print(t1,t2,t3,t4,t5,t6,t7)





    def main(self):
        self.professional_score_line()


if __name__ == '__main__':
    crawler = Crawler()
    crawler.main()