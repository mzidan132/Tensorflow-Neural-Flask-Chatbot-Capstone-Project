import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, TimeDistributed, RepeatVector, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Example dataset
data = [
    ("Hi", "Hello"),
    ("How are you?", "I'm fine, thank you!"),
    ("What is your name?", "I'm a chatbot."),
    ("Goodbye", "Bye! Have a nice day!")
]

# Split the dataset into input (questions) and output (responses)
input_texts, target_texts = zip(*data)

# Tokenize the texts
tokenizer = Tokenizer()
tokenizer.fit_on_texts(input_texts + target_texts)
input_sequences = tokenizer.texts_to_sequences(input_texts)
target_sequences = tokenizer.texts_to_sequences(target_texts)

# Pad sequences
max_seq_length = max(len(seq) for seq in input_sequences + target_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_seq_length, padding='post')
target_sequences = pad_sequences(target_sequences, maxlen=max_seq_length, padding='post')

# Prepare the data for the LSTM model
X = np.array(input_sequences)
y = np.array(target_sequences)

# Define the model
vocab_size = len(tokenizer.word_index) + 1  # Plus 1 for padding token
embedding_dim = 50
lstm_units = 64

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_seq_length),
    LSTM(lstm_units, return_sequences=True),
    TimeDistributed(Dense(vocab_size, activation='softmax'))
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# Train the model
model.fit(X, np.expand_dims(y, -1), epochs=100, batch_size=2)

# Function to generate a response
def generate_response(input_text):
    input_sequence = tokenizer.texts_to_sequences([input_text])
    input_sequence = pad_sequences(input_sequence, maxlen=max_seq_length, padding='post')
    prediction = model.predict(input_sequence)
    response_sequence = np.argmax(prediction, axis=-1)
    response_text = tokenizer.sequences_to_texts(response_sequence)
    return response_text[0]

# Test the chatbot
test_input = "How are you?"
response = generate_response(test_input)
print(f"Input: {test_input}\nResponse: {response}")
