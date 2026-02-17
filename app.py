from flask import Flask, render_template, request
import joblib
import re
import os

app = Flask(__name__)

# Load the models
email_model = joblib.load('Email/phishing_rf_pipeline.pkl')
url_model = joblib.load('Url/rf_phishing_model.pkl')
tfidf_vectorizer = joblib.load('Url/tfidf_vectorizer.pkl')


def is_url(input_text):
    """Simple check if string is a URL."""
    url_regex = re.compile(
        r'(https?://)?([a-zA-Z0-9.-]+)\.[a-zA-Z]{2,}([/?].*)?'
    )
    return url_regex.match(input_text.strip()) is not None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']

        if is_url(input_text):
            # If '-' in URL, classify as Phishing
            if '-' in input_text:
                prediction = 2  # 2 = Phishing
            else:
                url_features = tfidf_vectorizer.transform([input_text])
                prediction = url_model.predict(url_features)[0]
            result_type = "URL"
        else:
            # Email classification
            prediction = email_model.predict([input_text])[0]
            result_type = "Email"

        # Format prediction name
        if result_type == "URL":
            if str(prediction).lower() == "benign":
                pred_label = "Legitimate"
            elif str(prediction) == "0":
                pred_label = "Legitimate"
            elif str(prediction) == "2" or str(prediction).lower() == "phishing":
                pred_label = "Phishing"
            else:
                pred_label = str(prediction)
        elif result_type == "Email":
            pred_label = "Phishing" if prediction == 1 else "Legitimate"

        return render_template('index.html', input_text=input_text,
                               result=f'{result_type} classified as: {pred_label}')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
