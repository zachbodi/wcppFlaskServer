from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    barcode = path
    return barcode

if __name__ == "__main__":
    app.debug = True
    app.run()
