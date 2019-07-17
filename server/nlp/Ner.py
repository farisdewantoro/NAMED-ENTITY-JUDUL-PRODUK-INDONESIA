from sklearn_crfsuite import metrics
from sklearn_crfsuite import scorers
import sklearn_crfsuite
from sklearn.metrics import make_scorer, classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import scipy.stats
import sklearn
from itertools import chain
from nltk.tag import CRFTagger
import pandas as df
import os
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pickle
from collections.abc import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.tokenize import RegexpTokenizer
import csv
from pprint import pprint
from joblib import dump, load
GLOBAL_INDEX = 0
stemmer = StemmerFactory().create_stemmer()


def word2features(sent, i):

    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, postag, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


MAP_ENTITY_TAG = {
    "TYPE": "TYPE",  # 2119
    "BRAND": "BRAND",  # 1099
    "NAME": "NAME",  # 733
    "COLOR": "COLOR",  # 414
    "MATERIAL": "MATERIAL",  # 202
    "THEME": "THEME",  # 161
    "DIMENSION": "DIMENSION",  # 148
    "GENDER": "GENDER",  # 140
    "SIZE": "SIZE",  # 122
    "MASS": "MASS",  # 95
    "AGE": "AGE",  # 74
    "SHAPE": "SHAPE",  # 30
    "CAPACITY": "CAPACITY",  # 52
    "RAM": "RAM",  # 24
    "OS": "OS",  # 15
    "PROCESSOR": "PROCESSOR",  # 14
    "GRAPHIC": "GRAPHIC",  # 7
    "STORAGE": "STORAGE",  # 7
    "DISPLAY": "DISPLAY",  # 5
    "MEMORY": "MEMORY",  # 5
    "CPU": "CPU",  # 4
    "CAMERA": "CAMERA",  # 4
}

TAGGER3 = CRFTagger()

TAGGER3.set_model_file(os.path.abspath(
    'server/nlp/data/all_indo_man_tag_corpus_model.crf.tagger'))


def getPOSTag(_temporary_tokens):
    strin = []
    for token_tag in _temporary_tokens:
 
        if token_tag[0].encode('ascii', 'ignore').decode('utf8'):
            strin.append(token_tag[0].encode('ascii', 'ignore').decode('utf8'))
    return [(str(token.encode('ascii', 'ignore'), 'utf8'), str(tag.encode('ascii', 'ignore'), 'utf8')) for (token, tag) in TAGGER3.tag_sents([strin])[0]]


def getPOSTagTesting(_temporary_tokens):
    strin = []
    for token_tag in _temporary_tokens:
        if token_tag.encode('ascii', 'ignore').decode('utf8'):
            strin.append(token_tag.encode('ascii', 'ignore').decode('utf8'))
    return [(str(token.encode('ascii', 'ignore'), 'utf8'), str(tag.encode('ascii', 'ignore'), 'utf8')) for (token, tag) in TAGGER3.tag_sents([strin])[0]]


def getTypeData(_ne):
    """
    ekstrak jenis Name Entity
    """
    l_regex = re.compile(r"\<ENAMEX\s+TYPE\=\"")
    r_regex = re.compile(r"\"\>[^<]+\<\/ENAMEX\>")
    a = r_regex.sub(r'\0', l_regex.sub(r'\0', _ne))

    """
    ekstrak data Name Entity
    """
    r = re.compile(r"\<ENAMEX\s+TYPE\=\"\w+\"\>")
    s = re.compile(r"\<\/ENAMEX\>")
    b = s.sub(r'\0', r.sub(r'\0', _ne))

    """
    Hapus karakter bukan alfabet dari jenis Name Entity
    """
    entity = re.sub(r'[^\w]', '', a), b

    return entity


def checkEntities(data):
    l_regex = re.compile(r"\<ENAMEX\s+TYPE\=\"")
    r_regex = re.compile(r"\"\>[^<]+\<\/ENAMEX\>")
    a = r_regex.sub(r'\0', l_regex.sub(r'\0', data))
    return a


def parseEntity(data):
    temporary_tokens = []
    entities_name = re.findall(
        r"\<ENAMEX\s+TYPE\=\"\w+\"\>[^<]+\<\/ENAMEX\>", data)

    temp = []

    list_entity = []
    for entity_name in entities_name:

        ne_type, ne_data = getTypeData(entity_name)

        check_if_exist = list(
            filter(lambda x: x == ne_type.strip(), list(MAP_ENTITY_TAG.keys())))

        if check_if_exist:

            temp = data.strip().split(entity_name, 1)
            cek_failed_entity = re.compile("<ENAMEX")

            if temp[0] and (cek_failed_entity.search(temp[0]) == None):

                for token in temp[0].strip().split(' '):

                    word = token.replace('\x00', '')
                    # hilangkan semua karakter kecuali number dan huruf apabila panjannya hanya 1
                    filter_character = re.search('^[^a-zA-Z\d\s:]$', word)
                    if word and not filter_character:

                        temporary_tokens.append((word, 'O'))
            ne_data_split = ne_data.strip().split(' ')
            wordx = ne_data_split[0].replace('\x00', '')

            if wordx:

                temporary_tokens.append(
                    (wordx, "B-" + MAP_ENTITY_TAG[ne_type.replace('\x00', '')]))

            if len(ne_data_split) > 1:
                for i in range(len(ne_data_split) - 1):
                    word = ne_data_split[i + 1].replace('\x00', '')
                    if word:
                        temporary_tokens.append(
                            (word, "I-" + MAP_ENTITY_TAG[ne_type.replace('\x00', '')]))
            data = temp[1]

            if len(temp) > 1:
                if temp[1] and (cek_failed_entity.search(temp[1]) == None):

                    for token in temp[1].strip().split(' '):

                        word = token.replace('\x00', '')
                        # hilangkan semua karakter kecuali number dan huruf apabila panjannya hanya 1
                        filter_character = re.search('^[^a-zA-Z\d\s:]$', word)
                        if word and not filter_character:

                            temporary_tokens.append((word, 'O'))
        else:
            pass

    result = []
    if(temporary_tokens):

        postageed = getPOSTag(temporary_tokens)
 
        for i in range(len(temporary_tokens)):
            str_postagged = None
            print(postageed)
            print(50*"=")
            str_append = (postageed[i][0], postageed[i][1], str(
                temporary_tokens[i][1].encode('ascii', 'ignore'), 'utf8'))
            result.append(str_append)

    return result


train_data = []
train_test = []


class NER:
    def __init__(self):
        self.file_path = os.path.abspath(
            'server/nlp/data/data_train2.txt')
        self.tokenize = RegexpTokenizer(r'\w+')
        self.crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )

    def train(self):
        model = os.path.abspath(
            'server/nlp/data/model.joblib')
        if os.path.exists(model):
            model = load(os.path.abspath(
                'server/nlp/data/model.joblib'))
            self.crf = model
            return model
        else:
            crf = self.crf
            f = open(self.file_path)
            lines = [line for line in f.read().split("\n")]
            f.close()
            for row in lines:
                if parseEntity(row):
                    train_data.append(parseEntity(row))

            # for row in lines[500:]:
            #     if parseEntity(row):
            #         train_test.append(parseEntity(row))
            X_train = [sent2features(s) for s in train_data]
            y_train = [sent2labels(s) for s in train_data]
            # X_test = [sent2features(s) for s in train_test]
            # y_test = [sent2labels(s) for s in train_test]
            # print(train_data[0])
            crf.fit(X_train, y_train)
          
            # state_features = crf.state_features_
            # out = zip(state_features.keys(), state_features.values())
            # with open(os.path.abspath(
            #         'server/nlp/data/data_features.csv'), 'w', encoding="utf8",newline="") as csv_feature:
            #     writer = csv.writer(csv_feature)
            #     writer.writerow(['key','value'])
            #     for i in out:
            #         writer.writerow(i)
            # csv_feature.close()


            dump(crf, os.path.abspath(
                'server/nlp/data/model.joblib'))
            self.crf = crf
            return self.crf
    def predict_single(self,input_text):
        crf = self.crf
        labels = list(crf.classes_)
        # labels.remove('O')
        sorted_labels = sorted(
            labels,
            key=lambda name: (name[1:], name[0])
        )
        text_tokenize = self.tokenize.tokenize(input_text)
     
        text_pos = getPOSTagTesting(text_tokenize)
        text_feature = sent2features(text_pos)
        y_pred = crf.predict_single(text_feature)
        # print(list(zip(y_pred,text_tokenize)))
        result = [list(zip(y_pred,text_tokenize))]
       
        return result
    def cfm(self):
        crf = self.crf
        f = open(self.file_path)
        lines = [line for line in f.read().split("\n")]
        f.close()
        train_test = []

        for row in lines[1500:]:
            if parseEntity(row):
                train_test.append(parseEntity(row))
        for row in lines[:1500]:
            if parseEntity(row):
                train_data.append(parseEntity(row))
        X_train = [sent2features(s) for s in train_data]
        y_train = [sent2labels(s) for s in train_data]
        X_test = [sent2features(s) for s in train_test]
        y_test = [sent2labels(s) for s in train_test]
 
        crf.fit(X_train, y_train)
        labels = list(crf.classes_)
        new_classes = labels.copy()
        new_classes.remove('O')
        # print(rows)
        # train_test = [parseEntity(row) for row in rows]
        y_pred = crf.predict(X_test)
   
        return metrics.flat_classification_report(
                y_test, y_pred, labels=new_classes, digits=3
            )
        # return make_scorer(y_pred=per.predict(X_test), y_true=y_test, labels=new_classes)
            



# print(ner.cfm())
# ner.train()
# text_input = [
#     'Lumin HD90 Camcorder Digital Camera 1080P 12MP Video Full HD DV DVR 2.7 TFT LCD 16x Zoom',
#     'Apple iPhone 6s 16GB Garansi Distributor 1 Tahun',
#     'Apple iPhone Xr 128GB SG SET - 3/128GB White Black Red Blue Yellow Coral',
#     'Theclover kemeja pria lengan pendek ASGARD 10warna 4 SIZE M-L-XL-xxl/kemeja pria Slim Fit/kemeja kombi batik',
#     'HP Gaming Mouse M100 7 LED - Hitam.',
#     'Jaket Parka Taslan Waterproof - Oenzie Store'
# ]

# for i in text_input:
#     y_pred = ner.predict_single(i)
#     print(y_pred)
#     print(60*"=")


# pd = df.read_csv('data_test/baju.csv')
# for i in pd.iterrows():
#     i[1]['title']
