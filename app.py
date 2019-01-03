
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

#create Flask instance
app = Flask(__name__)

#use Flask pymongo to set up a conncetion
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

#Route that will render info using template
@app.route("/")
def display():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars_data = mars_data)

#Route that will trigger scraping
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = mission_to_mars.scrape()
    mars.update({}, mars_data, upsert = True)
    return redirect("/", code = 302)

#Required code to run app
if __name__ == "__main__":
    app.run(debug = True)