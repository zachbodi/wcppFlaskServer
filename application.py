from flask import Flask
from key import KEY
import mysql.connector
import requests
import json

application = Flask(__name__)

mydb = mysql.connector.connect(
	host="wcppdatabase.ckosxabna9k7.us-east-2.rds.amazonaws.com",
	user="admin",
	passwd="Qf4Tzvi&7J##UxUgjDVz",
	database="appData"
)

@application.route("/")
def home():
	return "Hello, World!"

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
	url = "https://api.edamam.com/api/food-database/parser?app_id=bb34f199&app_key={}&upc={}".format(KEY, path) 
	response = requests.get(url)
	product = response.json()
    
	try:
		ingredients = product["hints"][0]["food"]["foodContentsLabel"]
		ingredients = ingredients.lower()
		ingredients = ingredients[:ingredients.index('.')]
		ingredients = ingredients.replace('[', ';')
		ingredients = ingredients.replace('.', '')
		ingredients = ingredients.replace(']', '')
		ingredients = ingredients.replace(' (',', ')
		ingredients = ingredients.replace('), ', ', ')
		ingredients = ingredients.replace('(','')
		ingredients = ingredients.replace(')','')
		ingredients = ingredients.replace('*','')
		ingredients = ingredients.replace(' and ',', ')
		ingredients = ingredients.replace(",", ";")
		ingredients = ingredients.split(";")
		ingredients = [x.strip() for x in ingredients]

		outputResponse = {"tested": []}
		mycursor = mydb.cursor()
		for ingredient in ingredients:
			mycursor.execute("SELECT light FROM chemicals WHERE name LIKE '%{}%'")
			sqlResponse = mycursor.fetchall()
			for row in sqlResponse:
				outputResponse.tested.append((ingredient, str(row)))
		return str(outputResponse)
	except:
		if "error" in product:
			return "null"
		raise Exception("something went wrong in processing")

if __name__ == "__main__":
    application.run(host='localhost',port=8080,debug=True)
