from bs4 import BeautifulSoup
from urllib import request


def kamera_digital():
    page = request.urlopen(
        'https://id.wikipedia.org/wiki/Daftar_merek_kamera_digital')
    soup = BeautifulSoup(page, features='html.parser')
    ol = soup.find('ol')
    return ol.find_all('li')

def write_file(file_name,data):
    with open(file_name, 'a+', newline="\n", encoding="utf8") as file:
            for d in data:
                file.write(d.get_text()+'\n')
            file.close()


write_file('MEREK.txt', kamera_digital())
