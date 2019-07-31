from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pprint import pprint
import re
import json
import csv
from flask_socketio import emit
from ..nlp import NER


def check_next(bot):
    root = bot.find_element_by_class_name("cpF1IH")
    li_tag = root.find_elements_by_tag_name("li")
    a_tag = li_tag[2].find_element_by_tag_name("a").get_attribute("href")
    return a_tag


def stop_find(bot):
    try:
        not_found = bot.find_element_by_class_name("c1nVRb")
        if not_found:
            print(50*'=')
            print('FINISH')
            return False
        else:
            return True
    except Exception as ex:
        return True


class DetikBot():
    def __init__(self):
        self.keyword = ''
        self.isRunning = False
        self.NER = NER()
        self.NER.train()
        self.key_tagged = None
        self.list_article = []

    def start_bot(self, keyword):
        self.isRunning = True
        self.keyword = keyword

    def stop_bot(self):
        self.isRunning = False
        self.keyword = ''
        print(self.isRunning)

    def predict_keyword(self, data):
        ner = self.NER
        return ner.predict_single(data)

    def get_weights_target(self):
        ner = self.NER
        return ner.weight_targets()

    def get_transition_features(self):
        return self.NER.transition_features()
    def get_article(self,bot):
        ner = self.NER
        try:
            root = WebDriverWait(bot, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            root_judul = root.find_element_by_class_name('jdl')
            judul = root_judul.find_element_by_tag_name('h1').text
            date = root_judul.find_element_by_class_name('date').text

            root_image = root.find_element_by_class_name('pic_artikel')
            img = root_image.find_element_by_tag_name('img').get_attribute('src')

            root_detail = root.find_element_by_class_name('detail_wrap')
            detail = root_detail.find_element_by_class_name('itp_bodycontent').text
            d = ner.predict_single(detail)
            new_d = list(filter(lambda x: x[0] != 'O', d[0]))
            print(new_d)
            result = {
                "judul": judul,
                "date":date,
                "img":img,
                "detail":d
            }
            if result:
                emit('response_search_detik',result)
            
            return True
        except Exception as ex:
            print(ex)
            return None

 
    def filter_url(self,url):
        match = re.match(
            r'^(https://news.detik.com)',url)

        print(match)
        if match:
            return True
        else:
            return False
        
    def search(self,bot):
        bot.execute_script(
            f'document.getElementsByName("query")[0].setAttribute("value","{self.keyword}")')
        bot.execute_script(
            'document.getElementsByClassName("dtkframebar__icons dtkframebar__icons-search")[0].click()')
        # _input = root_form.find_element_by_class_name("text")
        bot.execute_script(
            "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
        )
        list_result = WebDriverWait(bot, 40).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-berita"))
            )
        list_berita_article = list_result.find_elements_by_tag_name('article')
        list_url = []
        for i in list_berita_article:
            if i.get_attribute('class'):
                   pass
            else:
                list_url.append(i.find_element_by_tag_name(
                    'a').get_attribute("href"))

        return list_url
            # try:
            #    print(i.get_attribute('class').size())
            #    if i.get_attribute('class'):
            #        pass
            # except:
            #     print(i.get_attribute('innerHTML'))
            # if i.get_attribute('class').size() == 0:
            #     print(i.get_attribute('innerHTML'))
        # _input.send_keys('jokowi')
    def run_finding(self):
        # key = self.NER.predict_single(self.keyword.strip())

        # return
        # emit('ner_keyword', self.key_tagged)
        # print(self.key_tagged)
        # print(50*"=")
        # print(self.key_tagged[0].index('B-TYPE'))
        bot = webdriver.Firefox()
        bot.set_window_position(0, 0)
        bot.set_window_size(500, 480)
        bot.get(
            f"https://www.detik.com/"
        )
        time.sleep(1.5)
        list_url = self.search(bot)
        new_list = list(filter(self.filter_url, list_url))
        # print(list_url)
        
        for i in new_list:
            bot.get(i)
            time.sleep(0.3)
            bot.execute_script(
                "window.scrollTo({top:600,left:0,behavior: 'smooth'})"
            )
            self.get_article(bot)
            time.sleep(3)
            if not self.isRunning:
                break
      
        # list_p = bot.find_elements_by_class_name("c5TXIP")
        # product_list = []
        # first_product = map(self.get_list, list_p)
        # # emit('response_search_lazada', json.dumps(list(first_product)))
        # # with open(f"{self.keyword}.csv", "w", newline="", encoding="utf-8") as csv_file:
        # #     fieldnames = [
        # #         "title",
        # #         "link",
        # #         "price_now",
        # #         "location",
        # #         "discount_price",
        # #         "discount_percent",
        # #         "img_link",
        # #     ]
        # #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # #     writer.writeheader()
        # for list_p in first_product:
        #       emit('response_search_lazada', json.dumps(list_p))
        #     # writer.writerow(list_p)
        # # product_list.append(list(first_product))

        # pagination = check_next(bot)
        # i = 1
        # if not pagination:
        #     self.isRunning = False
        # while self.isRunning:
        #     i += 1
        #     link = re.sub(r"page=(\d)$", f"page={i}", pagination)
        #     print(link)
        #     bot.get(link)

        #     bot.execute_script(
        #         "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
        #     )
        #     time.sleep(2.5)
        #     keep_run = stop_find(bot)
        #     if not keep_run:
        #         self.isRunning = False
        #     list_p = bot.find_elements_by_class_name("c5TXIP")
        #     product = map(self.get_list, list_p)
            # emit('response_search_lazada', json.dumps(list(product)))
            # with open(f"{self.keyword}.csv", "a", newline="", encoding="utf-8") as csv_file:
            #     fieldnames = [
            #         "title",
            #         "link",
            #         "price_now",
            #         "location",
            #         "discount_price",
            #         "discount_percent",
            #         "img_link",
            #     ]
            #     writer = csv.DictWriter(csv_file, fieldnames)
            # for list_p2 in product:
            #     if list_p2 and self.isRunning:
            #         emit('response_search_lazada', json.dumps(list_p2))
              
