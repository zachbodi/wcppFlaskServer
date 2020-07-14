from flask import Flask
from key import KEY, sqluser, sqlpass
import mysql.connector
import requests
import json

application = Flask(__name__)

mydb = mysql.connector.connect(
	host="wcppdatabase.ckosxabna9k7.us-east-2.rds.amazonaws.com",
	user=sqluser,
	passwd=sqlpass,
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
		name = product["hints"][0]["food"]["label"]
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
		ingredients = [{"name":x.strip(), "light":"green"} for x in ingredients]

		output = {"name":name, "ingredients":ingredients}
		mycursor = mydb.cursor()
		for i in range(len(ingredients)):
			mycursor.execute("SELECT light FROM chemicals WHERE name LIKE '%{}%'")
			sqlResponse = mycursor.fetchall()
			for row in sqlResponse:
				ingredients[i].light = str(row)
		return str(json.dumps(output))
	except:
		if "error" in product:
			return "null"
		raise Exception("something went wrong in processing")

if __name__ == "__main__":
    application.run()
