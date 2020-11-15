import nltk

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import WordPunctTokenizer
from spacy.lang.ru import Russian

nltk.download('stopwords')

stopwords = set(stopwords.words('russian'))
stopwords.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','#','№'])

lemmer = Russian()
stemmer = SnowballStemmer(language='russian')
tokenizer = WordPunctTokenizer()

def filter_words(text: str ) -> str:
  tokens = []
  for token in tokenizer.tokenize(text):
    if token not in stopwords and not token.isdigit():
      tokens.append(token)
  return " ".join(tokens)

def lemmatization(text: str) -> str:
  tokens = [token.lemma_ for token in lemmer(text)]
  return " ".join(tokens)

def stemming(text: str) -> str:
  tokens = [stemmer.stem(w) for w in tokenizer.tokenize(text)]
  return " ".join(tokens)

def clean(text: str) -> str:
  text = filter_words(text)
  text = lemmatization(text)
  text = stemming(text)
  return text
