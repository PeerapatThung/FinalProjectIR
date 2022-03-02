import pickle
import re
import string
from pathlib import Path

import pandas as pd
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean(text):
    cleaned_text = text.translate(str.maketrans('', '', '!"#$%&\'()*+,.<=>?@[]^`{|}~' + u'\xa0'))
    cleaned_text = cleaned_text.lower()
    cleaned_text = cleaned_text.translate(str.maketrans(string.whitespace, ' ' * len(string.whitespace), ''))
    tokenized_text = word_tokenize(cleaned_text)
    stop_dict = {s: 1 for s in stopwords.words()}
    sw_removed_text = [word for word in tokenized_text if word not in stop_dict]
    sw_removed_text = [word for word in sw_removed_text if len(word) > 2]
    ps = PorterStemmer()
    stemmed_text = ' '.join([ps.stem(w) for w in sw_removed_text])
    return stemmed_text
dataset = pd.read_csv('ingredient_dataset.csv')
dataset = dataset.drop(['Unnamed: 0', 'Ingredients'],axis=1)
dataset = dataset.dropna()
dataset = dataset.reset_index(drop=True)
cleaned_title = []

if not Path('cleaned_title.pickle').exists():
    for i in dataset['Title']:
        cleaned_title.append(clean(i))
    with open('cleaned_title.pickle', 'wb') as fin:
        pickle.dump(cleaned_title, fin)
else:
    with open('cleaned_title.pickle', 'rb') as fin:
        cleaned_title = pickle.load(fin)



# description = dataset['Title']
# stop_dict = {s: 1 for s in stopwords.words()}
# ps = PorterStemmer()
# cleaned_description = description.apply(lambda s: s.translate(str.maketrans('', '',string.punctuation + u'\xa0')))
# cleaned_description = cleaned_description.apply(lambda s: s.lower())
# cleaned_description = cleaned_description.apply(lambda s: word_tokenize(s))
# cleaned_description = cleaned_description.apply(lambda s: [word for word in s if word not in stop_dict])
# cleaned_description = cleaned_description.apply(lambda s: [word for word in s if len(word) > 2])
# cleaned_description = cleaned_description.apply(lambda s: ' '.join([ps.stem(w) for w in s]))

def query(input):
    tfidfvectorizer = TfidfVectorizer(ngram_range=(1,2))
    title_vec = tfidfvectorizer.fit_transform(cleaned_title)
    query = tfidfvectorizer.transform([clean(input)])
    result = cosine_similarity(title_vec, query).reshape((-1,))
    for i, index in enumerate(result.argsort()[-10:][::-1]):
        print(str(i + 1), dataset['Title'][index], "--", dataset['Cleaned_Ingredients'][index], "--", result[index])
