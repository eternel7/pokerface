import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from unidecode import unidecode
import json
from chatrooms.queries import get_key_synonyms

# import gensim.downloader as gensim

# download the model and return as object ready for use
# model_gensim_wiki = gensim.load("glove-wiki-gigaword-100")

defaultImage = "/static/img/icons/apple-touch-icon-76x76.png"

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
try:
    nltk.data.find('corpora/omw')
except LookupError:
    nltk.download('omw')


def lemTokens(tokens):
    return [nltk.stem.WordNetLemmatizer().lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), " ") for punct in string.punctuation)


def lemNormalize(text):
    return lemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


wn.ensure_loaded()
freqs = {}
freqs['english'] = nltk.FreqDist(w for w in wn.words())
freqs['french'] = nltk.FreqDist(w for w in wn.words(lang='fra'))


def cleanText(t):
    # no accent
    txt = unidecode(t)
    # not case sensitive
    txt = txt.lower()
    # no punctuation
    return txt.translate(remove_punct_dict)


def textToKeys(text, lang):
    lang = 'english' if lang != 'fr' else 'french'
    # tokenize the pattern
    words = nltk.word_tokenize(cleanText(text))
    words = [w for w in words if w.isalpha()]
    all_words = words[:]  # creating a copy of the words list
    words_filtered = words[:]  # creating a copy of the words list
    # remove stop words
    stop_words = stopwords.words(lang)
    for word in words:
        if word in stop_words:
            words_filtered.remove(word)
    
    # do not leave empty the word array
    if len(words_filtered) == 0:
        words_filtered = all_words
    
    wn.ensure_loaded()
    final_words = []
    
    # use freq in synonyms to purge and normalize word array
    for word in words_filtered:
        freq = 0
        chosen_one = word
        for syn in wn.synsets(word):
            for s in syn.lemmas():
                syn_n = s.name()
                if freqs[lang][syn_n] > freq:
                    chosen_one = cleanText(syn_n)
                    freq = freqs[lang][syn_n]
        if freqs[lang][chosen_one] > 0:
            final_words.append(chosen_one)
    
    final_words.sort()
    # search for user validated synonyms
    syn_keys = get_key_synonyms(json.dumps(final_words))
    if syn_keys:
        return json.loads(syn_keys)
    
    return final_words


def findClosestText(text, texts_to_compare):
    texts_to_compare_clean = []
    for t in texts_to_compare:
        texts_to_compare_clean.append(cleanText(t))
    texts_to_compare_clean.append(text)
    TfidfVec = TfidfVectorizer(tokenizer=lemNormalize)
    tfidf = TfidfVec.fit_transform(texts_to_compare_clean)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        return None
    else:
        return {"text": texts_to_compare[idx], "score": req_tfidf}
