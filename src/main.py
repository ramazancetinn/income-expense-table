from flask import Flask, request, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_pyfile("config.py")

mysql = MySQL(app)

@app.route('/')
def home():
   # cur = mysql.connection.cursor()
   # cur.execute("SELECT * FROM user;")
   # users = cur.fetchall()
   # cur.close()
   return render_template("home.html", **locals())
@app.route('/add_income', methods=['POST'])
def add_income():
   income_date = request.json["income_date"]
   income_type = request.json["income_type"]
   income_explanation = request.json["income_explanation"]
   income_price = request.json["income_price"]
   cur = mysql.connection.cursor()
   cur.execute(f"""INSERT INTO income (income_type, income_explanation, income_price, income_date)
                                 VALUES ('{income_type}', '{income_explanation}', '{income_price}', '{income_date}')""")
   mysql.connection.commit()
   cur.close()
   return "success"

@app.route('/add_expense', methods=['POST'])
def add_expense():
   expense_date = request.json["expense_date"]
   expense_type = request.json["expense_type"]
   expense_explanation = request.json["expense_explanation"]
   expense_price = request.json["expense_price"]
   cur = mysql.connection.cursor()
   cur.execute(f"""INSERT INTO expense (expense_type, expense_explanation, expense_price, expense_date)
                                 VALUES ('{expense_type}', '{expense_explanation}', '{expense_price}', '{expense_date}')""")
   mysql.connection.commit()
   cur.close()
   return "success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

