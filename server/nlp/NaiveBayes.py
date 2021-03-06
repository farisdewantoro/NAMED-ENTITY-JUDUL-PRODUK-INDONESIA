from sklearn.metrics import make_scorer, classification_report
from nltk.tag import CRFTagger
import pandas as df
import nltk
import os
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pickle
from collections.abc import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI
from nltk.chunk import conlltags2tree, tree2conlltags, accuracy
from nltk.tokenize import RegexpTokenizer
import csv
from pprint import pprint
from joblib import dump, load
GLOBAL_INDEX = 0
stemmer = StemmerFactory().create_stemmer()

def features(tokens, index, history):
    global GLOBAL_INDEX

    if(index == 0):
        GLOBAL_INDEX += 1
        # print("kalimat ke- ", GLOBAL_INDEX)
        """
        `tokens`  = a POS-tagged sentence [(w1, t1), ...]
        `index`   = the index of the token we want to extract features for
        `history` = the previous predicted IOB tags
        """
   
    # Pad the sequence with placeholders
    tokens = [('[START2]', '[START2]'), ('[START1]', '[START1]')] + \
        list(tokens) + [('[END1]', '[END1]'), ('[END2]', '[END2]')]
    history = ['[START2]', '[START1]'] + list(history)

    # shift the index with 2, to accommodate the padding
    index += 2
    word, pos = tokens[index]
    prevword, prevpos = tokens[index - 1]
    prevprevword, prevprevpos = tokens[index - 2]
    nextword, nextpos = tokens[index + 1]
    nextnextword, nextnextpos = tokens[index + 2]
    previob = history[index - 1]
    contains_dash = '-' in word
    contains_dot = '.' in word
    allascii = all([True for c in word if c in string.ascii_lowercase])

    allcaps = word == word.capitalize()

    capitalized = word[0] in string.ascii_uppercase

    prevallcaps = prevword == prevword.capitalize()
    prevcapitalized = prevword[0] in string.ascii_uppercase

    nextallcaps = prevword == prevword.capitalize()
    nextcapitalized = prevword[0] in string.ascii_uppercase
    
    nextWord_3 = nextword[-3:] if nextpos != '[END1]' and nextpos != '[END2]' else nextword
    nextWord_2 = nextword[-2:] if nextpos != '[END1]' and nextpos != '[END2]' else nextword

    nextNextWord_3 = nextnextword[-3:] if nextnextword != '[END1]' and nextnextword != '[END2]' else nextnextword
    nextNextWord_2 = nextnextword[-2:] if nextnextword != '[END1]' and nextnextword != '[END2]' else nextnextword

    prevWord_3 = prevword[-3:] if prevword != '[START2]' and prevword != '[START1]' else prevword
    prevWord_2 = prevword[-2:] if prevword != '[START2]' and prevword != '[START1]' else prevword

    prevPrevWord_3 = prevprevword[-3:] if prevprevword != '[START2]' and prevprevword != '[START1]' else prevprevword
    prevPrevWord_2 = prevprevword[-2:] if prevprevword != '[START2]' and prevprevword != '[START1]' else prevprevword

    hasil_feature = {
        'word': word,
        'word[-3]':word[-3:],
        'word[-2]':word[-2:],
        'word.isdigit()': word.isdigit(),
        # 'lemma': stemmer.stem(word),
        'pos': pos,
        'all-ascii': allascii,

        'next-word': nextword,
        'next-word[-3]': nextWord_3,
        'next-word[-2]': nextWord_2,
        # 'next-lemma': stemmer.stem(nextword),
        'next-pos': nextpos,

        'next-next-word': nextnextword,
        'next-next-word[-3]': nextNextWord_3,
        'next-next-word[-2]': nextNextWord_2,
        'nextnextpos': nextnextpos,

        'prev-word': prevword,
        'prev-word[-3]': prevWord_3,
        'prev-word[-2]': prevWord_2,
        # 'prev-lemma': stemmer.stem(prevword),
        'prev-pos': prevpos,

        'prev-prev-word': prevprevword,
        'prev-prev-word[-3]': prevPrevWord_3,
        'prev-prev-word[-2]': prevPrevWord_2,
        'prev-prev-pos': prevprevpos,

        'prev-iob': previob,


        'all-caps': allcaps,
        'capitalized': capitalized,

        'prev-all-caps': prevallcaps,
        'prev-capitalized': prevcapitalized,

        'next-all-caps': nextallcaps,
        'next-capitalized': nextcapitalized,
    }
    remove = [i for i in hasil_feature.keys() if hasil_feature[i] == '[START2]' or hasil_feature[i]
              == '[START1]' or hasil_feature[i] == '[END1]' or hasil_feature[i] == '[END2]']

    for k in remove:
        del hasil_feature[k]
        # if hasil_feature[i] == '[START2]' or hasil_feature[i] == '[START1]' or hasil_feature[i] == '[END1]' or hasil_feature[i] == '[END2]':
        #     del hasil_feature[i]
        
    # pprint(hasil_feature)
    return hasil_feature


class NamedEntityChunker(ChunkParserI):
    def __init__(self, train_sents, **kwargs):
       
        assert isinstance(train_sents, Iterable)
        
        self.feature_detector = features
       
        self.tagger = ClassifierBasedTagger(
            train=train_sents,
            feature_detector=features,
            verbose=True,
            **kwargs)


    def parse(self, tagged_sent):

        chunks = self.tagger.tag(tagged_sent)
        # print(dir(self.tagger.tag))
        # print(self.tagger.tag)
        # Transform the result from [((w1, t1), iob1), ...]
        # to the preferred list of triplets format [(w1, t1, iob1), ...]
        iob_triplets = [(w, t, c) for ((w, t), c) in chunks]

        # Transform the list of triplets to nltk.Tree format
        return iob_triplets

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
    "CAPACITY": "CAPACITY",  # 52
    "SHAPE": "SHAPE",  # 30
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

            str_append = ((postageed[i][0], postageed[i][1]), str(
                temporary_tokens[i][1].encode('ascii', 'ignore'), 'utf8'))
            result.append(str_append)

    return result
class NER():
    def __init__(self):
        # self.file_path = os.path.abspath('server/nlp/data/data_train2.txt')
        self.file_path = os.path.abspath('server/nlp/data/data_train2.txt')
        self.tokenize = RegexpTokenizer(r'\w+')         
        self.train_data = []
        self._chunk = None
        self.tagger = None
    def train(self):
        model = os.path.abspath(
            '1server/nlp/data/model2.joblib')
        if os.path.exists(model):
         
            model = load(model)
            train_file = open(self.file_path)
            lines = [line for line in train_file.read().split("\n")]
            # train_file.close()
            train_ = []
            for row in lines:
                if parseEntity(row):
                    train_.append(parseEntity(row))
            # score = model.evaluate(
            #     train_[:1500]
            # )
            # data_test = [conlltags2tree(iobs) for iobs in train_[1500:]]
      
            self._chunk = model
            return model
        else:
            train_file = open(self.file_path)
            lines = [line for line in train_file.read().split("\n")]
            # train_file.close()
            train_=[]
            for row in lines:
                if parseEntity(row):
                    train_.append(parseEntity(row))
      
            self._chunk = NamedEntityChunker(train_)
            score = self._chunk.evaluate(
                [conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in train_[1500:]])

            print(score)
      
            dump(self._chunk, os.path.abspath(
                 'server/nlp/data/model2.joblib'))
            return self._chunk
    def predict_single(self, input_text):
        chunk = self._chunk
        # labels.remove('O')
        text_tokenize = self.tokenize.tokenize(input_text)

        text_pos = getPOSTagTesting(text_tokenize)
        y_pred = chunk.parse(text_pos)
        # print(text_pos,y_pred)
        # print(accuracy(chunk, text_pos))
        # print(list(zip(y_pred,text_tokenize)))
        # result = [list(zip(y_pred, text_tokenize))]
        label = [list(filter(lambda x:i.index(x) == 2, i))[0] for i in y_pred]
       
        result = [list(zip(label, text_tokenize))]
        return result




 
