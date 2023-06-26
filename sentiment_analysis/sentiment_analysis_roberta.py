# roBERTa with 3 classifications

import torch
from transformers import RobertaTokenizerFast, RobertaForSequenceClassification

tokenizer = RobertaTokenizerFast.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
model = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

def get_sentiment(text):
    # Preprocessing the text to be suitable for RoBERTa
    encoded_input = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')

    # Getting model's output
    output = model(**encoded_input)

    # The model returns the logits for each class. We take the softmax to get the probabilities.
    probabilities = torch.nn.functional.softmax(output.logits, dim=-1)
    probabilities_numpy = probabilities.detach().numpy()[0]

    class_predicted = torch.argmax(probabilities).item()

    # 'cardiffnlp/twitter-roberta-base-sentiment' is a model trained for sentiment analysis. It assigns 0 for negative, 1 for neutral, and 2 for positive sentiment.
    if class_predicted == 0:
        sentiment = "Negative"
    elif class_predicted == 1:
        sentiment = "Neutral"
    else:
        sentiment = "Positive"

    return sentiment, probabilities_numpy

example_text = [
    "That movie was not good.", # negative
    "That was a great meal we had!", # positive
    "They drove the car on the street.", # neutral
    "Did you see my e-mail?", # neutral
    "We are in a bull market.",
    "We are in"
    "Stocks surge after controversial election.", # positive
    "Company outlook bleak after disappointing earnings report.", #negative
    "Experts expect a bull market soon.", # positive
    "Bear market expected to continue through the next year.", # negative
    "Tech sector primed for growth amidst market turmoil." #positive or neutral
]

for text in example_text:
    sentiment, probabilities = get_sentiment(text)
    print(f"News: {text}\nSentiment: {sentiment}\nProbabilities: Negative {probabilities[0]}, Neutral {probabilities[1]}, Positive {probabilities[2]}\n")
