import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required resources (only needed once)
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

def clean_text(text: str, remove_stopwords: bool = True, lemmatize: bool = True) -> str:
    """
    Clean and prepare a string for NLP tasks.

    Args:
        text (str): The input text to clean.
        remove_stopwords (bool): Whether to remove English stopwords.
        lemmatize (bool): Whether to apply lemmatization.

    Returns:
        str: The cleaned text.
    """
    # Lowercase the text
    text = text.lower()

    # Remove punctuation and digits
    text = re.sub(rf"[{string.punctuation}]", " ", text)
    text = re.sub(r"\d+", "", text)

    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Remove stopwords
    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize tokens
    if lemmatize:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join tokens back into a string
    cleaned_text = " ".join(tokens)

    return cleaned_text