from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    # @TODO: YOUR CODE HERE!
    mars_rec = mongo.db.mars.find_one()
    return render_template("index.html", mars_data=mars_rec)
    # Return template and data
 
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    # @TODO: YOUR CODE HERE!
    mrs = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mrs.update({}, mars_data, upsert=True)
    return redirect("/", code=302)
    # Update the Mongo database using update and upsert=True
    # @TODO: YOUR CODE HERE!

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
