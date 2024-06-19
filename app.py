from flask import Flask, render_template, request, jsonify
import random
import nltk

app = Flask(__name__)

nltk.download('punkt')

# Load the movie lines
def load_lines(file_path):
    lines = {}
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        for line in file:
            parts = line.split(" +++$+++ ")
            lines[parts[0]] = parts[-1].strip()
    return lines

# Load the movie conversations
def load_conversations(file_path, lines):
    conversations = []
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        for line in file:
            parts = line.split(" +++$+++ ")
            convo_ids = eval(parts[-1])
            conversations.append([lines[id] for id in convo_ids if id in lines])
    return conversations

lines = load_lines('data/movie_lines.txt')
conversations = load_conversations('data/movie_conversations.txt', lines)

# Create a list of input-output pairs
input_output_pairs = []
for convo in conversations:
    for i in range(len(convo) - 1):
        input_output_pairs.append((convo[i], convo[i+1]))

def get_response(user_input):
    tokenized_input = nltk.word_tokenize(user_input.lower())
    responses = []
    for pair in input_output_pairs:
        if tokenized_input == nltk.word_tokenize(pair[0].lower()):
            responses.append(pair[1])
    if responses:
        return random.choice(responses)
    else:
        return "I don't understand. Can you ask something else?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    message = request.json.get('message')
    response = get_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
