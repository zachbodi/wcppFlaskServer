from flask import Flask

application = Flask(__name__)

@application.route("/")
def home():
    return "Hello, World!"

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    barcode = path
    return barcode

if __name__ == "__main__":
    application.run(host='0.0.0.0',port=8080,debug=True)
