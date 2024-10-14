import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import string
import json
import os
from prompt import Prompt
from data import Data

# Reads information from the json and uses that data to predict future data.

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    # Return the preprocessed text as a string
    return ' '.join(lemmatized_tokens)

vectorizer = None
classifier = None


# TODO: Create check before running that checks if items.json has enough entries to start predicting

# Load data
def load():
    try:
        data = Data()
        data.mainloop()
        file = 'items.json'
        if not os.path.exists(file):
            file = Prompt.get_file()
        file = open('items.json', 'r')
        
        data = json.load(file)
        expenses_data = [(entry["description"], entry["category"]) for entry in data]
    except IOError as e:
        print(e)

    # Preprocess expenses data
    X = [preprocess_text(expense[0]) for expense in expenses_data]
    y = [expense[1] for expense in expenses_data]

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a TF-IDF vectorizer
    global vectorizer
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)

    # Train a logistic regression classifier
    global classifier
    classifier = LogisticRegression()
    classifier.fit(X_train_vectorized, y_train)
    return

def predict(entries):
    # Predict categories for new expenses
    X_new = [preprocess_text(expense) for expense in entries.keys()]
    X_new_vectorized = vectorizer.transform(X_new)
    predicted_categories = classifier.predict(X_new_vectorized)

    # Initialization of a dictionary of categories and their costs
    output = {}

    # Output predicted categories for new expenses
    for expense, category in zip(entries, predicted_categories):
        if output.get(category) is not None:
            output[category].update({expense:entries[expense]})#[expense]
        else:
            output[category] = {expense:entries[expense]}
    return output

