from flask import Flask ,  render_template , url_for ,redirect , request
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Database setup  
# client = MongoClient('mongodb://localhost:27017/') # local MongoDB server
load_dotenv()  # .env loading

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
todo_tbl = db['todo_tbl']
contact_tbl = db['contact_tbl']
users_tbl = db['users_tbl']

# Cloudinary config
cloudinary.config(
    cloud_name="dtupm0mck",
    api_key="142211981314583",
    api_secret="V5yAg39l6qvqXOv7oYteyiJjiL4"
)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

# @app.route("/home")
# def home():
#     return "Welcome to home"


@app.route("/index")
def index():
    # fetch all data from database
    todos = list(todo_tbl.find())
    return render_template('index.html' , data = todos)



@app.route("/contact")
def contact ():
    return render_template('contact.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        users_tbl.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users_tbl.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error='Invalid credentials')
    return render_template('signin.html')

@app.route("/logout")
def logout():
    return redirect(url_for('login'))

@app.route("/add" , methods = ['POST'])
def add_todo():
    title = request.form.get('title')
    desc = request.form.get('desc')
    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result['secure_url']
    todo_tbl.insert_one({
        'title': title , 
        'desc': desc,
        'image_url': image_url
        })
    return redirect(url_for('index'))

@app.route("/submit-contact", methods=["POST"])
def submit_contact():   
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    contact_tbl.insert_one({
        'name': name,
        'email': email,
        'message': message
    })

    # Here you can process the data, e.g., store it in the database or send an email
    print(f"Received contact form submission: Name={name}, Email={email}, Message={message}")

    return redirect(url_for('contact'))

#----------- delete route -----------#
@app.route("/delete/<id>")
def delete_todo(id):
    todo_tbl.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

#----------- update route -----------#
@app.route("/update/<id>" , methods=["GET"])
def update_form(id):
    todo = todo_tbl.find_one({'_id': ObjectId(id)})
    return render_template('update.html' , todo = todo)

@app.route("/update/<id>" , methods=["POST"])
def update_todo(id):
    title = request.form.get('title')
    desc = request.form.get('desc')
    update_data = {'title': title, 'desc': desc}
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            upload_result = cloudinary.uploader.upload(file)
            update_data['image_url'] = upload_result['secure_url']
    todo_tbl.update_one(
        {'_id': ObjectId(id)} , 
        {'$set': update_data}
        )
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)