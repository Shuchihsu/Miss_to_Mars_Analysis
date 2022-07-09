from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
# Create the Flask instance
# __name__ is the name of the current Python module. 
# The app needs to know where it’s located to set up some paths, and __name__ is a convenient way to tell it that.
app = Flask(__name__)

# Use flask_pymongo to set up Mimongo connection
# tells python that our app will connect to Mongo using a URI(a uniform resource identifies similar to a URL)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Tells Flask what to display when we're looking at the home page, index.html
@app.route("/")
def index():
    # use PyMongo to find mars tables/collection in our database
    mars =mongo.db.mars.find_one()
    #index.html is the default HTML file that we'll use to display the content we've scraped
    # tell Flask to return an HTML template  using an index.html file.
    # mars = mars , variable = mars.collection. tells Python to use the mars collection in MongoDB
    return render_template("index.html",mars =mars)

@app.route("/scrape")
def scrape():
    # new variable (mars) point to our Mongo database
    mars =mongo.db.mars
    # mars_data hold the scraped data
    # we have another file call scraping.py. Here we are referencing the scrap_all function in the scraping.py file which is exported from Jupyter Notebook.
    mars_data = scraping.scrape_all()
    # update the database
    # .update_one(query_parameter,{"$set":data},options). the query_parameter can be {"news_title": "Mars Landing Successful"} or empty{}. 
    # so we can update a document with a matiching news_title or leave empy{} to update the first matching doc in the collection.
    # $set means modified. $set: data
    # A 302 redirect code is a way to tell a search engine that you have temporarily relocated your site to a new URL 
    # and that it should forward any traffic intended for the old address to the temporary location.
    # This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).
    mars.update_one({},{"$set":mars_data},upsert = True)
    return redirect('/',code = 302)
    # Tells Flask to run
if __name__ == "__main__":
    app.run()
    #if __name__ == “main”: is used to execute some code only if the file was run directly, and not imported.???