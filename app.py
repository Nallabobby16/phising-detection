from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('model/phishing_model.pkl')

# Function to extract features (match training features)
def extract_features(url):
    features = {
        'url_length': len(url),
        'num_special_chars': sum([1 for c in url if c in ['@', '.', '-', '_', '~', '&', '=', '/']])
    }
    return pd.DataFrame([features])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect_phishing', methods=['POST'])
def detect_phishing():
    data = request.get_json()
    url = data.get('url', '')

    # Extract features and make a prediction
    features = extract_features(url)
    prediction = model.predict(features)[0]

    result = {'isPhishing': bool(prediction)}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
