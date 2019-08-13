from sklearn_crfsuite import metrics
from sklearn_crfsuite import scorers
import sklearn_crfsuite
from sklearn_crfsuite.utils import flatten
from sklearn.metrics import make_scorer, classification_report, confusion_matrix,multilabel_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import sys
import scipy.stats
import sklearn
import string
from itertools import chain
from nltk.tag import CRFTagger
import pandas as df
import os
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from collections.abc import Iterable
from nltk.tag import ClassifierBasedTagger
from nltk.chunk import ChunkParserI
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.tokenize import RegexpTokenizer,word_tokenize
import csv
from pprint import pprint
from joblib import dump, load
import eli5
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter
import pandas as pd
GLOBAL_INDEX = 0
stemmer = StemmerFactory().create_stemmer()
factory = StopWordRemoverFactory()
stopwords = factory.get_stop_words()
from pycrfsuite import ItemSequence
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))
def word2features(sent, i):
    
    word = sent[i][0]
    
    postag = sent[i][1]
 
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'hasNumber': hasNumbers(word),

        'word[-3:]': word[-3:],
        # 'word[-2:]': word[-2:],
        'word[:3]': word[:3],
        # 'word[:2]': word[:2],
        'stopword':True if word in stopwords else False,
     
        'postag': postag,
        # 'postag[:2]': postag[:2],
  
        
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:word.isdigit()': word1.isdigit(),
            '-1:hasNumber': hasNumbers(word1),
            '-1:stopword': True if word1 in stopwords else False,
            '-1:postag': postag1,

            # '-1:word[-3:]': word1[-3:],
            # '-1:word[-2:]': word1[-2:],
            # '-1:word[:3]': word1[:3],
            # '-1:word[:2]': word1[:2],
            # '-1:postag[:2]': postag1[:2],
            
        })
    else:
        features['BOS'] = True #kalimat diposisi awal

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:word.isdigit()': word1.isdigit(),
            '+1:hasNumber': hasNumbers(word1),
            '+1:stopword': True if word1 in stopwords else False,
            '+1:postag': postag1,
            # '+1:postag[:2]': postag1[:2],
            # '-1:word[-3:]': word1[-3:],
            # '-1:word[-2:]': word1[-2:],
            # '-1:word[:3]': word1[:3],
            # '-1:word[:2]': word1[:2],
        })
    else:
        features['EOS'] = True #kalimat diposisi akhir
  
    
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
    "O":"O",
    # "GRAPHIC": "GRAPHIC",  # 7
    # "STORAGE": "STORAGE",  # 7
    # "DISPLAY": "DISPLAY",  # 5
    # "MEMORY": "MEMORY",  # 5
    # "CPU": "CPU",  # 4
    # "CAMERA": "CAMERA",  # 4,
	# "ORGANIZATION": "ORG",
	# "LOCATION": "LOC",
	# "PERSON": "PER",

    # "BATTERY": "BATTERY",
    # "YEAR": "YEAR",
    # "GRAPHICS": "GRAPHICS",
    # "PATTERN": "PATTERN",
    # "FLAVOR": "FLAVOR",
    # "CLASS": "CLASS",
    # "AUTHOR": "AUTHOR",
    # "MOTIVE": "MOTIVE",
    # "ZOOM": "ZOOM",
    # "QUANTITY":"QUANTITY",
    # "CURRENT": "CURRENT",
    # "INTERNAL": "INTERNAL",
    # "NETWORK": "NETWORK",
    # "POWER": "POWER",
    # "RESOLUTION": "RESOLUTION",
    # "USB": "USB",
    # "VOLTAGE": "VOLTAGE",
    # "QUOTA": "QUOTA",
    # "FRAGRANCE": "FRAGRANCE",
    # "CARAT": "CARAT",
    # "SPEED": "SPEED",
    # "OUTPUT": "OUTPUT",
    # "VIDEO": "VIDEO",
    # "LENS": "LENS",
    # "VOLUME": "VOLUME",
    # "FLAVOUR": "FLAVOUR",
    # "SPEC": "SPEC",
    # "TECHNOLOGY": "TECHNOLOGY",
    # "CHARGE": "CHARGE",
    # "APERTURE": "APERTURE",
    # "STRENGTH": "STRENGTH",
    # "FRAGRANT": "FRAGRANT",
    # "KEY TYPE": "KEY TYPE",
    # "KEY BRAND": "KEY BRAND",
    # "KEY_TYPE": "KEY_TYPE",
    # "KEY_BRAND": "KEY_BRAND",
    # "KEY_NAME": "KEY_NAME",
    # "KEY_OS": "KEY_OS",
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

def filterEntities(data):
    not_ne_list = []
    for ne in data:
        ne_type, ne_data = getTypeData(ne)
        if ne_type not in list(MAP_ENTITY_TAG.keys()):
            not_ne_list.append(ne_type)
    if len(not_ne_list) > 0:
        return False
    else:
        return True
    
                
def checkEntities(data):
    
    l_regex = re.compile(r"\<ENAMEX\s+TYPE\=\"")
    r_regex = re.compile(r"\"\>[^<]+\<\/ENAMEX\>")
    a = r_regex.sub(r'\0', l_regex.sub(r'\0', data))
    if a.strip() in list(MAP_ENTITY_TAG.keys()):
        print(a)
    else:
        print('ga',a)
    return a


# re.I insensitive matching; untuk huruf besar dan huruf kecil sama
START_PATTERN = re.compile(r'^(.*?)<ENAMEX$', re.I)
END_SINGLE_PATTERN = re.compile(r'^TYPE="(.*?)">(.*?)</ENAMEX>(.*?)$', re.I)
TYPE_PATTERN = re.compile(r'^TYPE="(.*?)">(.*?)$', re.I)
END_MULTI_PATTERN = re.compile(r'^(.*?)</ENAMEX>(.*?)$', re.I)
EOS_PATTERN = re.compile(r'^([^<>]*)\.?\t(\d+)$', re.I)
NON_ENTITY_TYPE = 'O'


def check_and_process_eos(token):
    match = re.match(EOS_PATTERN, token)
  
    if match:
        print('ada nih',match)
        result.append((match.group(1),cur_type))
        # out.write(match.group(1) + '\t' + cur_type + '\n')
        # out.write('.' + '\t' + 'I-'+cur_type + '\n')
        # out.write('\n')
        return True
    return False


infile = os.path.abspath(
    'server/nlp/data/data_train2.txt')
outfile = os.path.abspath(
    'server/nlp/data/data_train5.csv')


def WorParser(data):
    cur_type = NON_ENTITY_TYPE
    temporary_tokens = []
    for token in data.strip().split(' '):
        token = token.strip()
        m = re.match(r'^((?!\d).)$', token)
        
        if not token or m:
            continue
    
        match = re.match(START_PATTERN, token)
        if match:
            if match.group(1):
                temporary_tokens.append((match.group(1), NON_ENTITY_TYPE))
            continue

        match = re.match(END_SINGLE_PATTERN, token)
        if match:

            # print(match.group(1), match.group(2))
            temporary_tokens.append((match.group(2), 'B-' + match.group(1)))
            cur_type = NON_ENTITY_TYPE
            
            if not check_and_process_eos(match.group(3)) and match.group(3):
         
                # print(match.group())
                temporary_tokens.append((match.group(3), cur_type))
                # out.write(match.group(3) + '\t' + cur_type + '\n')
            continue

        match = re.match(TYPE_PATTERN, token)
        if match and match.group(2):

            cur_type = match.group(1)
            temporary_tokens.append((match.group(2), 'B-'+cur_type))
            # out.write(match.group(2) + '\t'+'B-' + cur_type + '\n')
            continue

        match = re.match(END_MULTI_PATTERN, token)
        if match and (match.group(1) or match.group(2)):
            if cur_type != 'O' and not re.match(r'^(I-|B-)', cur_type):
                cur_type = 'I-'+cur_type
            temporary_tokens.append((match.group(1), cur_type))
            # out.write(match.group(1) + '\t' + 'I-'+cur_type + '\n')
            cur_type = NON_ENTITY_TYPE
            if not check_and_process_eos(match.group(2)) and match.group(2):
                temporary_tokens.append((match.group(2), cur_type))
                # out.write(match.group(2) + '\t' + cur_type + '\n')
            continue

        if check_and_process_eos(token):
            continue
        if cur_type != 'O' and not re.match(r'^(I-|B-)',cur_type):
            cur_type = 'I-'+cur_type
        temporary_tokens.append((token, cur_type))
        # out.write(token + '\t' + cur_type + '\n')
 
    result = []
    if(temporary_tokens):
       
        postageed = getPOSTag(temporary_tokens)
     
        # result.append(postageed)
        for i in range(len(temporary_tokens)):
            str_postagged = None
            ne_ = temporary_tokens[i][1]
            ne_temporary = re.sub(r'^(B-|I-)','',ne_)
            if ne_temporary not in list(MAP_ENTITY_TAG.keys()):
                
                ne_ = 'O'
            # print(postageed,temporary_tokens[i][1])
            str_append = (postageed[i][0], postageed[i][1], ne_)
            
            result.append(str_append)
    # print(result)
    return result




train_data = []
train_test = []

def re_format_for_csv(data):
    data_t = []

    for i in range(len(data)):
        for value in range(len(data[i])):
            d = list(data[i][value])
            d.insert(0, i)
            data_t.append(d)
            # for v in range(len(data[i][value])):
    # data_r = []
    data_r = []

    for i in range(len(data_t)):
        d = data_t[i][0]
        dd = data_t[i].copy()
        del dd[0]
        check = list(filter(lambda x:x[0] == d,data_r))

        if len(check) > 0:
            for data_index in range(len(data_r)):
                if data_r[data_index][0] == d:
                    data_r[data_index][1].append(dd)
        else:
            data_r.append([d, [dd]])
    return data_r

class NER:
    def __init__(self):
        self.file_path = os.path.abspath(
            'server/nlp/data/data_train2.txt')
        # self.file_path = os.path.abspath(
        #     'server/nlp/data/data_korpus_ne.txt')
        self.tokenize = RegexpTokenizer(r'\w+')
        self.encoding = None
        self.label_count = None
        self.crf = sklearn_crfsuite.CRF(
            algorithm='l2sgd',
            max_iterations=1000,
            all_possible_transitions=True,
            verbose=True,
            calibration_rate=0.1,
            calibration_eta=0.01
        )
    def one_hot_encoding(self,features):
        encoding = ItemSequence(features[0])
        self.encoding = encoding.items()
        return self.encoding
    def state_features_to_csv(self):
        data_frame = eli5.format_as_dataframes(
            eli5.explain_weights_sklearn_crfsuite(self.crf, top=10))
        data_frame['targets'].to_csv(os.path.abspath(
            'server/nlp/data/data_state_features.csv'))
        return 'ok'
    def transition_features_to_csv(self):
        data_frame = eli5.format_as_dataframes(
            eli5.explain_weights_sklearn_crfsuite(self.crf,top=2))
        data_frame['transition_features'].to_csv(os.path.abspath(
            'server/nlp/data/data_transition_features.csv'))
        return 'ok'
    def attributes_to_csv(self,model):
        with open(os.path.abspath('server/nlp/data/data_attributes.csv'), 'w', encoding="utf8", newline="") as data_attributes:
            writer = csv.writer(data_attributes)
            writer.writerow(['No', 'Attributes'])
         
            for k, i in model._info.attributes.items():
                writer.writerow([i, k])
        data_attributes.close()
        return 'ok'
    def print_transitions(self,trans_features):
        for (label_from, label_to), weight in trans_features:
            print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))
    def re_format_predict(self,data):
        result = []
        index = 0
        if len(data) > 0:
            for i in range(len(data[0])):
                _d = 'None'
                B = re.match(r'^(B-)', data[0][i][0])
                I = re.match(r'^(I-)', data[0][i][0])
                d = re.sub(r'^(B-|I-)', '', data[0][i][0])
                if i > 0:
                    _d = re.sub(r'^(B-|I-)', '', data[0][i-1][0])
                word = data[0][i][1]
                if B:
                    index = len(result)
                    result.append((d, [word]))
                if I:
                    if _d == d and word not in result[index][1]:
                        result[index][1].append(word)
                #     if any(key.get(B, None) == B for key in result):
                #         result.append(d)
        hasil_akhir = {}
        for i in result:
            if i[0] in hasil_akhir:
                hasil_akhir[i[0]].append(' '.join(i[1]))
            else:
                hasil_akhir[i[0]] = [' '.join(i[1])]
    
        return hasil_akhir
    def re_format(self,data):
        result = []
        for i in range(len(data)):
            B = re.match(r'^(B-)',data[i])
            I = re.match(r'^(I-)',data[i])
            d = re.sub(r'^(B-|I-)', '', data[i])
            _d = re.sub(r'^(B-|I-)', '', data[i-1])
            if B:
                result.append(d)
            elif I:
                if _d != d:
                    result.append(d)
            else:
                result.append(d)
        return result
    def re_format_class(self,data):
        labels = set(map(lambda x: re.sub(r'^(B-|I-)', '', x), data))
        return list(labels)
    def data_train_to_csv(self,data):
        data_r = re_format_for_csv(data)
        data_h = []
        for i in data_r:
            index = i[0]
            for val in i[1]:
                val.insert(0,index)
                data_h.append(val)


        with open(os.path.abspath(
            'server/nlp/data/data_train_transform.csv'), 'w', encoding="utf8",newline="") as data_train:
            writer = csv.writer(data_train)
            writer.writerow(['Word_row','Word','POS','Label'])
            for i in data_h:
                writer.writerow(i)
        data_train.close()
            # if :
            #     data_r.append([d,dd])
            # else:
            #     data_r.append()
            # if data_t[i][0] == i[0]:
            #     print(data_t[i][0], i[0])

        #     index = i[0]
        #     print(list(data_t[i]))
            # check = list(filter(lambda x: x[0] == index, data_r))
            
            # if len(check) > 0:

            #     print(data_r.index(check))
            #     pass
            # else:
            #     dd= list(i)
            #     del dd[0]
                
            #     data_r.append([index,[dd]])
             
                
        # print(data_r)
        # with open(os.path.abspath(
        #         'server/nlp/data/data_train.csv'), 'w', encoding="utf8",newline="") as data_train:
        #     writer = csv.writer(data_train)
        #     writer.writerow(['word_index','Word','POS','Label'])
        #     for i in data:
        #         for d in i:
        #             writer.writerow(i,d)
                
  
    def train(self):
        model = os.path.abspath(
            'server/nlp/data/model.joblib')
    
        if os.path.exists(model):
            model = load(model)
            self.crf = model
            pred=self.predict_single(
                'Acer Aspire 3 A315-41-R97J - AMD Ryzen R5 2500U - RAM 8GB - 1TB - Radeon RX Vega 8 - 15.6" - Windows 10 - Obsidian Black - Laptop Murah (Gratis Tas) - Bergaransi')
            # print(pred)
            return model
        else:
            print('CREATE MODEL')
            crf = self.crf
            # f = open(self.file_path)
            # lines = [line for line in f.read().split("\n")]
            # f.close()
            # train_test = []
            train_data = []
            # for row in lines:
            #     h = WorParser(row)
            #     # h = parseEntity(row)
            #     if h:
            #         train_data.append(h)

            dd = pd.read_csv(os.path.abspath(
                'server/nlp/data/data_train_transform.csv'))
          
            for i in range(len(dd)):
                dd_index = i

                _da = (dd['Word'][i],dd['POS'][i],dd['Label'][i])
                if i > 0 and dd['Word_row'][i] == dd['Word_row'][dd_index] and len(train_data)-1 >= dd['Word_row'][i]:
                    dd_index = i-1
                    train_data[dd['Word_row'][i]].append(_da)
                else:
                    train_data.append([_da])
            
               

  
            X = [sent2features(s) for s in train_data]
            Y = [sent2labels(s) for s in train_data]
            self.one_hot_encoding(X)
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, random_state=10)
            print(len(X_train),len(X_test))
            # X_test = [sent2features(s) for s in train_test]
            # y_test = [sent2labels(s) for s in train_test]
            # X_train = X
            # y_train = Y
            # print(train_data[0])
            crf.fit(X_train, y_train)
            labels = list(crf.classes_)
            new_classes = labels.copy()
            new_classes.remove('O')
            # print(rows)
            # train_test = [parseEntity(row) for row in rows]
            y_pred = crf.predict(X_test)
            score = metrics.flat_classification_report(
                y_test, y_pred, labels=new_classes, digits=3
            )

            print(score)
            # print("Top likely transitions:")
            # self.print_transitions(Counter(crf.transition_features_).most_common(20))

            # print("\nTop unlikely transitions:")
            # self.print_transitions(Counter(crf.transition_features_).most_common()[-20:])


            # y_true = flatten(y_test)
            # y_pred = flatten(y_pred)
            # re_format_labels = self.re_format_class(new_classes)
            # re_format_iob_y_true = self.re_format(y_true)
            # re_format_iob_y_pred = self.re_format(y_pred)
            
            # hasil  = multilabel_confusion_matrix(
            #     y_true, y_pred, labels=new_classes
            # )
            # np.set_printoptions(threshold=sys.maxsize)
            # tn = hasil[:, 0, 0]
            # tp = hasil[:, 1, 1]
            # fn = hasil[:, 1, 0]
            # fp = hasil[:, 0, 1]
            # print(hasil[:,])
            # pprint(tp / (tp + fp))
            # pprint(tp / (tp + fn))
            

            # print("Top likely transitions:")
            # self.print_transitions(Counter(crf.transition_features_).most_common(20))
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
        
         
            # weight = eli5.show_weights(crf, top=30)
            # print(dir(eli5))
          
            # for i in data_frame:
            #     print(data_frame[i])
            # pd = df.DataFrame(data_frame, index=True)
            # print(data_frame['targets'].to_html())
            # data_frame['targets'].to_csv(os.path.abspath(
            #     'server/nlp/data/data_feature_targets.csv'))
            # data_frame['transition_features'].to_csv(os.path.abspath(
            #     'server/nlp/data/data_transition_features.csv'))
            # pprint(dir(self.crf))
            # pprint(self.crf.state_features_)
            # pprint(self.crf.training_log_.iterations)
    
     
            return self.crf
    def weight_targets(self):
        data_frame = eli5.format_as_dataframes(
            eli5.explain_weights_sklearn_crfsuite(self.crf, top=2**10000))

        return list(zip(data_frame['targets']['target'], data_frame['targets']['feature'], data_frame['targets']['weight']))
    def transition_features(self):
        data_frame = eli5.format_as_dataframes(
            eli5.explain_weights_sklearn_crfsuite(self.crf))
        return list(zip(data_frame['transition_features']['from'],
                        data_frame['transition_features']['coef'], data_frame['transition_features']['to']))
    def predict_single(self,input_text):
        crf = self.crf
#         labels = list(crf.classes_)
#         # labels.remove('O')
#         sorted_labels = sorted(
#             labels,
#             key=lambda name: (name[1:], name[0])
#         )
        text_tokenize = self.tokenize.tokenize(input_text)
        # text_tokenize = word_tokenize(input_text)
        text_pos = getPOSTagTesting(text_tokenize)
        text_feature = sent2features(text_pos)
        y_pred = crf.predict_single(text_feature)

        # print(self.crf._tagger.probability(y_pred))
        # print(self.crf._tagger.marginal('I-AGE',2))

        # print(list(zip(y_pred,text_tokenize)))
        
        result = [list(zip(y_pred,text_tokenize))]

        return result, self.re_format_predict(result)
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
        score = metrics.flat_classification_report(
            y_test, y_pred, labels=new_classes, digits=3
        )
        print(score)
        return score
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
