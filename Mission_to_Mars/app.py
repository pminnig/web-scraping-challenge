
from flask import Flask, render_template
import pymongo
import scrape_mars
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_info

@app.route("/scrape")
def scraper():

    db.mars_info.drop()
    html_dict = scrape_mars.scrape()
    db.mars_info.insert_one(html_dict)
    return render_template("index.html", html_dict=html_dict)

@app.route("/")
def index():

    mars_stuff = dict(db.mars_info.find())
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)