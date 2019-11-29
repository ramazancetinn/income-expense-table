from flask import Flask, request, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_pyfile("config.py")

mysql = MySQL(app)

@app.route('/')
def home():
   return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

