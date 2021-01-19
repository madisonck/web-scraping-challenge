# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# establish Mongo connection via pymongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route that renders index.html template
@app.route("/")

def home():
        
    # find data in db
    mars_data = mongo.db.collection.find_one()

    # return template and data
    return render_template("index.html", mars=mars_data)

# create route that scrapes data
@app.route("/scrape")

def scrape():

    # execute scrape function
    web_scraped_data = scrape_mars.scrape()

    # revise Mongo database using update and upsert=True
    mongo.db.collection.update({}, web_scraped_data, upsert=True)

    # send to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)