from flask import Flask, render_template, request, jsonify
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
with open('knowledge_base.json', 'r') as f:
    knowledge_base = json.load(f)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)
preprocessed_contents = [preprocess_text(content) for content in knowledge_base.values()]
urls = list(knowledge_base.keys())
contents = list(knowledge_base.values())
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(preprocessed_contents)


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/enquire', methods=['POST'])
def enquire():
    user_input = request.json['user_input']
    response = process_enquiry(user_input)
    return jsonify({'response': response})


def process_enquiry(user_input):
    query = preprocess_text(user_input)
    predefined_responses = {
        'hello': 'Hello! How can I assist you today?',
        'hi': 'Hi there! How can I help you?',
        'hey': 'Hey! What can I do for you?',
        'thank you': 'You\'re welcome! Is there anything else you need?',
        'thanks': 'You\'re welcome! Is there anything else you need?',
    }

    for key in predefined_responses:
        if key in query:
            return predefined_responses[key]
    url, content = find_relevant_content(query, vectorizer, tfidf_matrix, urls, contents)
    return content
def find_relevant_content(query, vectorizer, tfidf_matrix, urls, contents):
    query_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    most_similar_idx = similarity_scores.argmax()
    return urls[most_similar_idx], contents[most_similar_idx]


if __name__ == '__main__':
    app.run(debug=True)
