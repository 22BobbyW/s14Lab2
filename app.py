import joblib
from flask import Flask, render_template

app = Flask(__name__)

# Load ML model
model = joblib.load('./notebooks/regr.pkl')

@app.route('/')
def index():
    # Make prediction - features = ['BEDS', 'BATHS', 'SQFT', 'AGE', 'LOTSIZE', 'GARAGE']
    prediction = model.predict([[4, 2.5, 3005, 15, 17903.0, 1]])[0][0].round(1)
    prediction = str(prediction)
    return render_template('index.html', pred=prediction)


@app.route('/world')
def hello_world():
    return 'Hello, World!'


@app.route('/<you>')
def hello_you(you):
    return f'Hello, {you}!'