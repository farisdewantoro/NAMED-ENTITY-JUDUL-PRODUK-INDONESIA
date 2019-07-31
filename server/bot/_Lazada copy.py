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


class LazadaBot():
    def __init__(self):
        self.keyword = ''
        self.isRunning = False
        self.NER = NER()
        self.NER.train()
        self.NER.predict_single('laptop asus warna hitam murah di bandung ram 8gb')
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
    def get_list(self,bot):
        try:
            ner = self.NER  
        
            # ROOT IMAGE
            root_img = WebDriverWait(bot, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "c2iYAv"))
            )
            img_a = root_img.find_element_by_class_name("cRjKsc")

            img_img = bot.find_element_by_class_name("c1ZEkM")
            # img_img = img_a.find_element_by_class_name('c1ZEkM')
            img_link = img_img.get_attribute("src")

            # ROOT DESKRIPTION
            root_desc = WebDriverWait(bot, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "c3KeDq"))
            )
            # root_desc = bot.find_element_by_class_name("c3KeDq")
            a_tag = root_desc.find_element_by_class_name("c16H9d").find_element_by_tag_name(
                "a"
            )
            # a_tag = root_link.find_element_by_tag_name("a")

            link = a_tag.get_attribute("href")
            # cari title dari tag A
            title = a_tag.get_attribute("title")

            # harga sekarang
            price_now = (
                root_desc.find_element_by_class_name("c3gUW0")
                .find_element_by_tag_name("span")
                .text
            )
            # harga diskon
            root_discount = root_desc.find_element_by_class_name("c3lr34")
            if root_discount.text:
                discount_price = root_discount.find_element_by_class_name(
                    "c13VH6").text
                discount_percent = root_discount.find_element_by_class_name(
                    "c1hkC1").text
            else:
                discount_price = None
                discount_percent = None
            location = (
                root_desc.find_element_by_class_name("c15YQ9")
                .find_element_by_class_name("c2i43- ")
                .text
            )
            if not img_link:
                img_link = False
            # final
            named_tag = ner.predict_single(title)
            
            data = {
                "title": title,
                "link": link,
                "price_now": price_now,
                "location": location,
                "discount_price": discount_price,
                "discount_percent": discount_percent,
                "img_link": img_link,
                "named_tag": named_tag
            }
            return data
        except Exception as ex:
            print(ex)
            return None

    def run_finding(self):
        # key = self.NER.predict_single(self.keyword.strip())

        # return
        # emit('ner_keyword', self.key_tagged)
        # print(self.key_tagged)
        # print(50*"=")
        # print(self.key_tagged[0].index('B-TYPE'))
        bot = webdriver.Firefox()
        bot.set_window_position(0, 0)
        bot.set_window_size(320, 480)
        bot.get(
            f"https://www.lazada.co.id/catalog/?q={self.keyword}&_keyori=ss&from=input&spm=a2o4j.searchlistcategory.search.go.45326184F3RgQ9"
        )
        time.sleep(1.5)

        bot.execute_script(
            "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
        )
        list_p = bot.find_elements_by_class_name("c5TXIP")
        product_list = []
        first_product = map(self.get_list, list_p)
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
        for list_p in first_product:
              emit('response_search_lazada', json.dumps(list_p))
            # writer.writerow(list_p)
        # product_list.append(list(first_product))

        pagination = check_next(bot)
        i = 1
        if not pagination:
            self.isRunning = False
        while self.isRunning:
            i += 1
            link = re.sub(r"page=(\d)$", f"page={i}", pagination)
            print(link)
            bot.get(link)

            bot.execute_script(
                "window.scrollTo({top:document.body.scrollHeight-1100,left:0,behavior: 'smooth'})"
            )
            time.sleep(2.5)
            keep_run = stop_find(bot)
            if not keep_run:
                self.isRunning = False
            list_p = bot.find_elements_by_class_name("c5TXIP")
            product = map(self.get_list, list_p)
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
       
            for list_p2 in product:
                if list_p2 and self.isRunning:
                    emit('response_search_lazada', json.dumps(list_p2))
                    # pprint(list_p2)
                    # writer.writerow(list_p2)
                       
