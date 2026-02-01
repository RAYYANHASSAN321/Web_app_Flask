from flask import Flask ,  render_template , url_for ,redirect , request
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Database setup  
# client = MongoClient('mongodb://localhost:27017/') # local MongoDB server
load_dotenv()  # .env load karega

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
todo_tbl = db['todo_tbl']



# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/home")
# def home():
#     return "Welcome to home"


@app.route("/index")
def index():
    return render_template('index.html')



@app.route("/contact")
def contact ():
    return render_template('contact.html')

@app.route("/add" , methods = ['POST'])
def add_todo():
    title = request.form.get('title')
    desc = request.form.get('desc')
    todo_tbl.insert_one({
        'title': title , 
        'desc': desc
        })
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)