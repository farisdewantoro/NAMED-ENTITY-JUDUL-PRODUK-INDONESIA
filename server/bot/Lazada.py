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
import asyncio



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


class LazadaBot():
    def __init__(self):
        self.keyword = ''
        self.isRunning = False
        self.NER = NER()
        self.NER.train()
        self.key_tagged =None
    def start_bot(self,keyword):
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

    def create_state_features_csv(self):
        return self.NER.state_features_to_csv()
    def create_csv_attribute(self):
        return self.NER.attributes_to_csv(self.NER.crf)
    def create_transition_features_csv(self):
        return self.NER.transition_features_to_csv()

    async def get_product_detail(self, url, bot):
        try:
            ner = self.NER 
            bot.get(url)
             # ROOT IMAGE
            root_container = WebDriverWait(bot, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#container"))
                )

            img = WebDriverWait(root_container, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".gallery-preview-panel__content img"))
                )

            title = bot.find_element_by_css_selector(
                ".pdp-mod-product-badge-title").text

            price = bot.find_element_by_css_selector(
                    ".pdp-product-price span").text
            location = bot.find_element_by_class_name(
                "location__address").text
            img_link = img.get_attribute("src")
            if not img_link:
                img_link = False
                # final
            named_tag,text_extraction = ner.predict_single(title)
           
            data = {
                "title": title,
                "link": url,
                "location": location,
                "price": price,
                "img_link": img_link,
                "named_tag": named_tag,
                "text_extraction": text_extraction
            }
            emit('response_search_lazada', json.dumps(data))
            # for url in list_url:
            #     time.sleep(7)
            #     try:
            #         if not self.isRunning:
            #             break
            #         bot.get(url)
            #         # ROOT IMAGE
            #         root_container = WebDriverWait(bot, 20).until(
            #             EC.presence_of_element_located(
            #                 (By.CSS_SELECTOR, "#container"))
            #         )
               
            #         img = WebDriverWait(root_container, 20).until(
            #             EC.presence_of_element_located(
            #                 (By.CSS_SELECTOR, ".gallery-preview-panel__content img"))
            #         )

            #         title = bot.find_element_by_css_selector(
            #             ".pdp-mod-product-badge-title").text
                
            #         price = bot.find_element_by_css_selector(
            #             ".pdp-product-price span").text
            #         location = bot.find_element_by_class_name("location__address").text
            #         img_link = img.get_attribute("src")
            #         if not img_link:
            #             img_link = False
            #         # final
            #         named_tag = ner.predict_single(title)
            #         print(named_tag)
            #         data = {
            #             "title": title,
            #             "link": url,
            #             "location": location,
            #             "price": price,
            #             "img_link": img_link,
            #             "named_tag": named_tag
            #         }
            #         emit('response_search_lazada', json.dumps(data))
             
            #     except Exception as ex:
            #         print('disini bro ',ex)
            #         pass
            # return 'mantap'
        except Exception as ex:
            print('ERROR',ex)
            return None
    def get_list_url(self,bot):
        try:
            root = bot.find_elements_by_css_selector('.cRjKsc a')
            list_url = [url.get_attribute("href") for url in root]
            return list_url
        except Exception as ex:
            print('ERROR DARI URL',ex)
            return None

    async def crawling(self, bot, pagination):
        i = 0
        while self.isRunning:
            i += 1
            if i != 1:
                link = re.sub(r"page=(\d)$", f"page={i}", pagination)
                bot.get(link)
                bot.execute_script(
                    "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
                )
            time.sleep(2.5)
            keep_run = stop_find(bot)
            if not keep_run:
                break
            list_url = self.get_list_url(bot)
            for url in list_url:
                if not self.isRunning:
                    break
                await self.get_product_detail(url, bot)
           
            print('index == ',i)
             
           

    def run_finding(self):
        GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.binary_location = GOOGLE_CHROME_PATH
        # bot = webdriver.Firefox()
        bot = webdriver.Chrome(
            execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        bot.set_window_position(0, 0)
        bot.set_window_size(320, 480)
        bot.get(
            f"https://www.lazada.co.id/catalog/?q={self.keyword}&_keyori=ss&from=input&spm=a2o4j.searchlistcategory.search.go.45326184F3RgQ9"
        )
        time.sleep(1.5)

        bot.execute_script(
            "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
        )
        pagination = check_next(bot)
        if not pagination:
            return 
        # list_url = self.get_list_url(bot)

        if self.isRunning:
            asyncio.run(self.crawling(bot, pagination))

      

    
        # list_p = bot.find_elements_by_class_name("cRjKsc")
        # product_list = []
        # first_product = map(self.get_list, list_p)
        # emit('response_search_lazada', json.dumps(list(first_product)))
        # with open(f"{self.keyword}.csv", "w", newline="", encoding="utf-8") as csv_file:
        #     fieldnames = [
        #         "title",
        #         "link",
        #         "price_now",
        #         "location",
        #         "discount_price",
        #         "discount_percent",
        #         "img_link",
        #     ]
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     writer.writeheader()
        # for list_p in first_product:
        #       emit('response_search_lazada', json.dumps(list_p))
            # writer.writerow(list_p)
        # product_list.append(list(first_product))

        # pagination = check_next(bot)
        # i = 1
        # if not pagination:
        #     self.isRunning = False
        # while self.isRunning:
        #     i += 1
        #     link = re.sub(r"page=(\d)$", f"page={i}", pagination)
        #     bot.get(link)

        #     bot.execute_script(
        #         "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
        #     )
        #     time.sleep(2.5)
        #     keep_run = stop_find(bot)
        #     if not keep_run:
        #         break
        #     list_p = bot.find_elements_by_class_name("c5TXIP")
        #     product = map(self.get_list, list_p)
        #     # emit('response_search_lazada', json.dumps(list(product)))
        #     # with open(f"{self.keyword}.csv", "a", newline="", encoding="utf-8") as csv_file:
        #     #     fieldnames = [
        #     #         "title",
        #     #         "link",
        #     #         "price_now",
        #     #         "location",
        #     #         "discount_price",
        #     #         "discount_percent",
        #     #         "img_link",
        #     #     ]
        #     #     writer = csv.DictWriter(csv_file, fieldnames)
       
        #     for list_p2 in product:
        #         if list_p2 and self.isRunning:
        #             emit('response_search_lazada', json.dumps(list_p2))
        #             # pprint(list_p2)
        #             # writer.writerow(list_p2)
                       
