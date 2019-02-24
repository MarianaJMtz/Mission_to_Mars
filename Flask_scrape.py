#Dependencies
from flask import Flask, render_template, redirect
from scrape_mars import scrape
from flask_pymongo import PyMongo

#Set up Flask
app = Flask(__name__)

#Set uo Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():

  results = mongo.db.results.find_one()
  return render_template('index.html', results=results)

@app.route("/scrape")
def scraper(): 
  
  results = mongo.db.results
  results_data = scrape()
  results.update({}, results_data, upsert=True)
  return redirect("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)
