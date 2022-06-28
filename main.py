#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:24:04 2022

@author: pramod
"""

import pandas as pd

from flask import Flask,render_template,request
import pickle

app=Flask(__name__)
data=pd.read_csv("Cleaned_data.csv")
pipe=pickle.load(open("RidgeModel.pkl","rb"))


@app.route("/")
def index():
    locations=sorted(data["location"].unique())
    return render_template("index.html",locations=locations)


@app.route("/predict",methods=["POST"])
def predict():
    location = request.form.get("location")
    bhk= request.form.get("bhk")
    bath=request.form.get("bath")
    sqft=request.form.get("total_sqft")
    a=[sqft,bhk,bath,location]
    a=[x for x in a if x!='']
    if len(a)==4:
        inputs =pd.DataFrame([[location,sqft,bath,bhk]],columns=["location","total_sqft","bath","bhk"])
        prediction=round(pipe.predict(inputs)[0]*100000,2)
        return "₹ "+str(prediction)
    else:
        return "Enter all fields"

    
    return str(a)
    
if __name__=="__main__":
    app.run(debug=True,port=5000)