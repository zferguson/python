# finBERT

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

def get_sentiment(text):
    # Preprocessing the text to be suitable for FinBERT
    encoded_input = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')

    # Getting model's output
    output = model(**encoded_input)

    # The model returns the logits for each class. We take the softmax to get the probabilities.
    probabilities = torch.nn.functional.softmax(output.logits, dim=-1)
    probabilities_numpy = probabilities.detach().numpy()[0]

    class_predicted = torch.argmax(probabilities).item()

    # 'ProsusAI/finbert' is a model trained for sentiment analysis. It assigns 0 for negative, 1 for neutral, and 2 for positive sentiment.
    if class_predicted == 0:
        sentiment = "Negative"
    elif class_predicted == 1:
        sentiment = "Neutral"
    else:
        sentiment = "Positive"

    return sentiment, probabilities_numpy

ambiguous_financial_news = [
    "Stocks surge after controversial election.", # positive
    "Company outlook bleak after disappointing earnings report.", #negative
    "Experts expect a bull market soon.", # positive
    "We are in a bear market.",
    "Bear market expected to continue through the next year.", # negative
    "Tech sector primed for growth amidst market turmoil." #positive or neutral
]

for news in ambiguous_financial_news:
    sentiment, probabilities = get_sentiment(news)
    print(f"News: {news}\nSentiment: {sentiment}\nProbabilities: Negative {probabilities[0]}, Neutral {probabilities[1]}, Positive {probabilities[2]}\n")
