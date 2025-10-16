from flask import Flask, jsonify, redirect, request

from base62_encoder import encode

import os, json

import random


app = Flask(__name__)

dataBaseFile = "data.json"

# For checking whether the json file exists or not 
if os.path.exists(dataBaseFile):
    
    with open(dataBaseFile, "r") as f:
        
        url_map = json.load(f)
else:
    
    url_map = {}  

def save_data():
    
    with open(dataBaseFile, "w") as f:

        json.dump(url_map, f, indent=4)
    
# URL Shortning function
@app.route("/shorten", methods = ["POST"]) 

def shorten():
    
    data = request.get_json()  # Gets the JSON File 
    
    longURL = data.get("url")  # Gets the url field from JSON File 
    
    if not longURL:
        return jsonify({"error" : "Url Missing"}), 400  # Url not present on JSON file 

    for code, url in url_map.items():       # check if url already exists

        if url == longURL:

            return jsonify({"short_url" : f"http://localhost:5000/r/{code}"})

    code = encode(random.randint(100000, 999999999)) # Generate base 62 code with a random number
    
    while code in url_map:
        code = encode(random.randint(100000, 999999999))
    
    url_map[code] = longURL  # map short url with long url 
    
    save_data()   # save the changes
    
    return jsonify({"short_url" : f"http://localhost:5000/r/{code}"}) # return shorten link
    
    
@app.route("/r/<code>")     # method = get, the default method

def redirectUrl(code):
    
    if code in url_map:
        return redirect(url_map[code])  # will redirect with the long url using short url
        
    return jsonify({"Error" : "url not found"}), 404    
    

@app.route("/")

def home():
    return jsonify({"message" : "Tiny Url Shortner API", "routes" : ["shorten(POST)", "/r/<code> (GET)"]})
    

if __name__ == "__main__":
    app.run(debug = True)

    
    



