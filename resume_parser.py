import fitz  # For PDF
import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Set your custom download path
NLTK_DATA_PATH = 'C:\\Users\\ZM COMPUTER\\AppData\\Local\\Programs\\Python\\Python313\\nltk_data'
nltk.data.path.append(NLTK_DATA_PATH)

# Ensure data is downloaded to the same path
nltk.download('punkt', download_dir=NLTK_DATA_PATH)
nltk.download('stopwords', download_dir=NLTK_DATA_PATH)

# Use the stopwords
stop_words = set(stopwords.words('english'))

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def clean_and_tokenize(text):
    # Lowercase and remove non-alphabetical characters
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)

    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return set(filtered_tokens)  # Return unique tokens for matching

