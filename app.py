import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import pickle
from flask import Flask, request, render_template

# Download NLTK resources only if needed
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.word_tokenize('test')
except LookupError:
    nltk.download('punkt')

# Preprocessor
ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word.isalnum()]
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]
    text = [ps.stem(word) for word in text]
    return " ".join(text)

# Flask setup
app = Flask(__name__)

# Load model and vectorizer
with open('model_1.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer_1.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        input_text = request.form['text']
        processed_text = transform_text(input_text)
        vectorized_text = vectorizer.transform([processed_text])
        result = model.predict(vectorized_text)[0]
        prediction = "Spam" if result == 1 else "Ham"
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
