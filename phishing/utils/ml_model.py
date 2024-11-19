import joblib
import os
import nltk

# from django.conf import settings

# Define the path to the model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "", "phishing_model.joblib")
VECTORIZER_PATH = os.path.join(BASE_DIR, "", "vectorizer.joblib")

try:
    phishing_model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except FileNotFoundError as e:
    phishing_model = None
    vectorizer = None
    print(f"Error loading model or vectorizer: {e}")

def preprocess_text(text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)