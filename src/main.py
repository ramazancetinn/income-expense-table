from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from datetime import datetime, timedelta, time
from flask import jsonify

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

@app.route('/endorsement', methods = ['GET', 'POST'])
def endorsement():
   
   date_time_str = datetime.today().strftime('%Y-%m-%d') 
   date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d' )
   to_date_default = date_time_obj.date().strftime('%Y-%m-%d')
   from_date_default = (date_time_obj.date() - timedelta(days=3)).strftime('%Y-%m-%d')

   
   
   if (request.method == 'POST' ):
      from_date = str(request.form['from'])
      
      if not request.form['to']:
         from_date = str(request.form['from'])
         to_date = from_date

               
      else:
         from_date = str(request.form['from'])
         to_date = str(request.form['to'])
   else:
      from_date = from_date_default
      to_date = to_date_default

   cur = mysql.connection.cursor()

   # Create income list with dates
   cur.execute("select * from income where (income_date between '{}' and '{}')".format(from_date, to_date))
   income_list = cur.fetchall()
   income_list = list(income_list)

   # Create expense list with dates
   cur.execute("select * from expense where (expense_date between '{}' and '{}')".format(from_date, to_date))
   expense_list = cur.fetchall()
   expense_list = list(expense_list)

   #Total income
   total_income = 0
   for i in income_list:
      total_income = total_income + int(i["income_price"])

   #Total expense
   total_expense = 0
   for i in expense_list:
      total_expense = total_expense + int(i["expense_price"])

   price_datas = { "total_income" : total_income,
                  "total_expense" : total_expense,
                  "diff"  : total_income-total_expense,
                  "time_period" : from_date +","+ to_date}

   print(price_datas)


   mysql.connection.commit()
   cur.close()


   return render_template("endorsement.html", **locals())

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

