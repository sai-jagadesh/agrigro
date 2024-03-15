import nltk
import json
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import pickle

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Load preprocessed data
data = pickle.load(open("chatbot_data.pkl", "rb"))
words = data['words']
classes = data['classes']
intents = data['intents']

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load trained model
model = Sequential()
model.add(Dense(128, input_shape=(len(words),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax'))
model.load_weights("chatbot_model.h5")

# Function to preprocess user input
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Function to create bag of words
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {w}")
    return(np.array(bag))

# Function to predict intent
def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Function to get response
def get_response(ints):
    tag = ints[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Main function to interact with chatbot
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = get_response(ints)
    return res
