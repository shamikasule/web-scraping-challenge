from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app= Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/marsscrape_app"

mongo=PyMongo(app)

@app.route("/")
def home():
    #Find one record of data from mongo db
    results = mongo.db.collection.find_one()
    
    #Return template and data
    return render_template("index.html", results=final_results)

#Route that will trigger scrape function
@app.route("/scrape")
#Code that lives in mongodb lives here
def scraper():
    #Run scrape function and save results to a variable
    data=scrape_mars.scrape()

    #Update Mongo db using update & upsert = True
    mongo.db.collection.update({}, data, upsert=True)

    # hemisphere_image_urls = mongo.db.hemisphere_image_urls
    # hemisphere_image_urls = scrape_mars.scrape()
    # hemisphere_image_urls.update({}, hemisphere_image_urls, upsert=True)

    #return back to home page (localhost:500) after scraping
    return redirect("/", code =302)


if __name__ == "__main__":
    app.run(debug=True)