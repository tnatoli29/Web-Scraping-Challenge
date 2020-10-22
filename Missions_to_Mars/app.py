#Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Set Flask up
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info = mars_info)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_info = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_info.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
