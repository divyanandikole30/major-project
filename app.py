from flask import Flask, request, render_template,redirect,jsonify,url_for
from flask_cors import CORS
import pandas as pd
import joblib
import json
import time
import datetime
from datetime import timedelta
import statsmodels.api as sm
import scipy.stats as stats
# from train import train
import sqlite3
import numpy as np
import pickle as pickle
import sqlite3
from sklearn.model_selection import train_test_split
import nltk
nltk.download('punkt')
import random
from flask import jsonify
import wikipedia

app = Flask(__name__)

model = joblib.load("model.sav")
scalerX = pickle.load(open("scalerX", "rb"))

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/signup")
def signup():
    name = request.args.get('username','')
    dob = request.args.get('DOB','')
    sex = request.args.get('Sex','')
    contactno = request.args.get('CN','')
    email = request.args.get('email','')
    martial = request.args.get('martial','')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `accounts` (`name`, `dob`,`sex`,`contact`,`email`,`martial`, `password`) VALUES (?, ?, ?, ?, ?, ?, ?)",(name,dob,sex,contactno,email,martial,password))
    con.commit()
    con.close()

    return render_template("login.html")

@app.route("/signin")
def signin():
    mail1 = request.args.get('uname','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `email`, `password` from accounts where `email` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("login.html")

    elif mail1 == data[0] and password1 == data[1]:
        return render_template("index.html")

    
    else:
        return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeRegressor
cls=DecisionTreeRegressor()

@app.route("/index1", methods=['POST', 'GET'])
def index1():
    if request.method == 'GET':
        return render_template("index1.html")
    elif request.method == 'POST':
        temperature = request.form['Temperature']
        humidity = request.form['Humidity']
        ph = request.form['PH']
        rainfall = request.form['Rainfall']
        N = request.form['Nitrogen']
        P = request.form['Phosphorus']
        K = request.form['Potassium']

        data = pd.read_csv('cpdata.csv')
        train = data.iloc[:, 0:7].values
        test = data.iloc[:, 8].values
        print(train)
        print(test)
        X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.3, random_state=0)
        cls.fit(X_train, y_train)
        prediction_data = cls.predict(X_test)
        X_live=[temperature,humidity,ph,rainfall,N,P,K]
        print(X_live)
        y_pred = cls.predict([X_live])
        print(y_pred,"##################################")
        to_predict=[temperature,humidity,ph,rainfall,N,P,K]
        resultt_ind=['rice','wheat','Mung Bean','Tea','millet','maize','Lentil','Jute','Coffee','Cotton','Ground Nut','Peas','Rubber','Sugarcane','Tobacco','Kidney Beans', 'Moth Beans','Coconut','Black Gram','Adzuki Beans','Pigeon Peas','Chickpea', 'banana','grapes', 'apple','Mango','Muskmelon','Orange','papaya', 'Pomegranate','Watermelon']
        result=resultt_ind[int(y_pred[0])]
        return render_template("result1.html", rf_result=result, to_predict=to_predict)
        # if str(y_pred) == '1.0':
        #     text='Crop name is rice'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
        # elif str(y_pred) == '2.0':
        #     text='crop name is wheat'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
        # elif str(y_pred) == '3.0':
        #     text='crop name is Mung Bean'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
        # elif str(y_pred) == '4.0':
        #     text='crop name is Tea'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
        # elif str(y_pred) == '5.0':
        #     text='crop name is millet'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
        # elif str(y_pred) == '6.0':
        #     text='crop name is maize'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
        # elif str(y_pred) == '7.0':
        #     text='crop name is Lentil'
        #     return render_template("result1.html", rf_result=text, to_predict=to_predict)
    return render_template("result1.html")

@app.route("/index", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        region = request.form['feedback1']
        season = request.form['attendance']
        production = request.form['feedback']
        cropname = request.form['overtime']

            
        to_predict = [season,production,cropname]
        

        rf_result = model.predict(scalerX.transform([to_predict]))

        

        if rf_result[0] == 0:
            remarks = 'Good'
            to_predict1 = [region,season,production,cropname,remarks]
            result = 'Prediction of Yield in that Region : Good'
            return render_template("result.html", rf_result=result,to_predict=to_predict1)

        else:
            remarks = 'Poor'
            to_predict1 = [region,season,production,cropname,remarks]
            result = 'Prediction of Yield in that Region : Poor'
            return render_template("result.html", rf_result=result,to_predict=to_predict1)
        
@app.route('/chatbot')
def chatbot():
    bot_response_url = url_for('get_bot_response')  
    return render_template("chatbot.html", bot_response_url=bot_response_url)




@app.route('/get_bot_response', methods=['POST'])
def get_bot_response():
    message = request.form['msg']
    response = ""

    greeting_responses = ["Hello!, enter the crop type", "Hi there!, enter the crop type", "Greetings!, enter the crop type"]
    goodbye_responses = ["Goodbye!", "See you later!", "Take care!"]

    crop_map = {
    "food": [
        "Common food crops include rice, wheat, corn, and vegetables.",
        "Food crops are essential for human consumption and provide essential nutrients.",
        "Farmers grow various food crops to feed people around the world."
    ],
    "cash": [
        "Cash crops are grown primarily for sale rather than for personal consumption.",
        "Examples of cash crops include cotton, coffee, tea, and sugarcane.",
        "Cash crops play a significant role in many economies by generating income for farmers."
    ],
    "industrial": [
        "Industrial crops are grown for non-food purposes, such as manufacturing or energy production.",
        "Examples of industrial crops include cotton, rubber, and oilseeds like soybeans.",
        "These crops are essential for producing goods like textiles, rubber products, and biofuels."
    ],
    "cover": [
        "Cover crops are planted primarily to manage soil erosion, fertility, and quality.",
        "Farmers often grow cover crops between main crops to protect and enrich the soil.",
        "Examples of cover crops include legumes, grasses, and certain types of clover."
    ],
    "perennial": [
        "Perennial crops live for several years and produce multiple harvests.",
        "Examples include fruit trees like apples and oranges, as well as perennial herbs like mint.",
        "Perennial crops require less replanting and are beneficial for soil health."
    ],
    "specialty": [
        "Specialty crops are grown in relatively small quantities and are often associated with specific regions or climates.",
        "Examples include niche fruits, exotic vegetables, and gourmet herbs.",
        "These crops cater to niche markets and often command higher prices."
    ],
    "rice": [
        "Rice is a staple food crop in many cultures around the world.",
        "Rice is a cereal grain that is cultivated in flooded fields called paddies or in well-drained soil.",
        "Rice can be grown in different climates, ranging from tropical to temperate regions."
    ]
}

    if message:
        tokens = nltk.word_tokenize(message.lower())

        if any(word in tokens for word in ["hello", "hi"]):
            response = random.choice(greeting_responses)
        elif any(word in tokens for word in ["goodbye", "bye"]):
            response = random.choice(goodbye_responses)
        else:
            crop_list = [w for w in tokens if w in crop_map]
            if crop_list:
                crop_category = crop_list[0]
                if crop_category == "specialty":
                    response = random.choice(crop_map[crop_category])
                elif crop_category == "food":
                    response = random.choice(crop_map[crop_category])
                elif crop_category == "cash":
                    response = random.choice(crop_map[crop_category])
                elif crop_category == "industrial":
                    response = random.choice(crop_map[crop_category])
                elif crop_category == "cover":
                    response = random.choice(crop_map[crop_category])
                elif crop_category == "perennial":
                    response = random.choice(crop_map[crop_category])
                elif crop_category == "rice":
                    response = random.choice(crop_map[crop_category])
                else:
                    response = "The crop name is " + crop_category
            else:
                response = "Sorry, I don't understand. Please enter the crop name"

    else:
        response = random.choice(greeting_responses)

    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=True)
