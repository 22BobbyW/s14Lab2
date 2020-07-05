from flask import Flask, render_template, request

app = Flask(__name__)

import joblib

# load ML model
linearModel = joblib.load('./notebooks/TTSModel.pkl')
trainTestSplit = joblib.load('./notebooks/TTSModel.pkl')
decisionTreeModel = joblib.load('./notebooks/DTModel.pkl')

# the data
beds = 4
baths = 2.5
sqft = 3005
age = 15
lotsize = 17903.0
garage = 1
reg = "linear"

@app.route('/')
def index():
    return render_template('index.html', prediction="", beds=beds, baths=baths, sqft=sqft, age=age, lotsize=lotsize, garages=garage, regression=reg)


@app.route('/sending/data', methods=['GET'])
def predict():

    print(request.args)

    if request.method == 'GET':
        beds = float(request.args['beds'])
        baths = float(request.args['baths'])
        sqft = float(request.args['sqft'])
        age = float(request.args['age'])
        lotsize = float(request.args['lotsize'])
        garage = float(request.args['garages'])
        reg = str(request.args['regressionType'])

        if reg == "linear":
            temp = linearModel.predict([[beds, baths, sqft, age, lotsize, garage]])[0][0].round(0)
            pred = ' (linear regression): ' + str(temp)
        elif reg == 'tree':
            temp = decisionTreeModel.predict([[beds, baths, sqft, age, lotsize, garage]])[0].round(0)
            pred = ' (decision tree regression): ' + str(temp)
        elif reg == 'tts':
            temp = trainTestSplit.predict([[beds, baths, sqft, age, lotsize, garage]])[0][0].round(0)
            pred = ' (train test split linear regression): ' + str(temp)
        else:
            pred = ': you did not chose a regression model :('
    else:
        print('error')

    prediction = "Housing Price Prediction" + str(pred)

    return render_template('index.html', prediction=prediction, beds=beds, baths=baths, sqft=sqft, age=age, lotsize=lotsize, garages=garage, regression=reg)
