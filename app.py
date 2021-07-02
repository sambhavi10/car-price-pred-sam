from flask import Flask,render_template,request
# import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

#create a Flask object
app  = Flask("car_model")

#create the ML model which we saved earlier in .pkl format
model = pickle.load(open('car_price_model.pkl','rb'))

#define the route(basically url) to which we need http request
#HTTP GET request method

@app.route('/',methods = ['GET'])

#create a function that will direct to index.html
def Home():
    return render_template('index.html')

#creating object for StandardScaler(used for scaling data)
standard_to = StandardScaler()

#HTTP POST request method
#defining the route for this post method
@app.route("/predict" ,methods = ['POST'])

def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':

        Year = int(request.form['Year'])
        Year = 2021 - Year
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']

        #converting into numerical values
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        
        elif(Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        
        #similarly for Sellet_type
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        
        #Transmission
        Transmission_Manual = request.form['Transmission_Manual']
        if(Transmission_Manual == 'Manual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        
        prediction = model.predict([[Present_Price,Kms_Driven2,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(prediction[0],2)

        if output<=0:
            return render_template('index.html',prediction_text = "Sorry, it isn't profitable to sell the car")
        else:
            return render_template('index.html', prediction_text = "You can sell the car for {} lacs".format(output))


    #html form to be displayed on screen when no values are inserted; without any output or prediction
    else:
        return render_template('index.html')

if __name__== "__main__":
    app.run(debug=True)

    
