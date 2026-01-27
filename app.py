from flask import Flask ,  render_template , url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/home")
def home():
    return "Welcome to home"


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/contact")
def contact ():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)