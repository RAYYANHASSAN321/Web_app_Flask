from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/home")
def home():
    return "Welcome to home"

if __name__ == "__main__":
    app.run(debug=True)