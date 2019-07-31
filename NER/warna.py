from bs4 import BeautifulSoup
from urllib import request


page = request.urlopen('https://id.wikipedia.org/wiki/Daftar_warna')
soup = BeautifulSoup(page, features='html.parser')
table = soup.find_all('table', {'class': 'wikitable'})

def data_warna_dasar():
    th = [th.get_text().replace('\n','') for th in table[0].find_all("th")]
    return th[5:]
def data_warna_lengkap():
    data = []
    for tr in table[1].find_all("tr"):
        if tr.find("td"):
            print(tr.find("td").get_text())
            data.append(tr.find("td").get_text().replace('\n', ''))
    return data
 
def write_file():
        with open('NER_WARNA.txt','w',newline="\n",encoding="utf8") as file:
                for wd in data_warna_dasar():
                        file.write(wd+'\n')
                for wl in data_warna_lengkap():
                        file.write(wl+'\n')
                file.close()

write_file()
