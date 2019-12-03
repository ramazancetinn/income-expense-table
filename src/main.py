from flask import Flask, request, render_template, flash,session,redirect,url_for,Response
from flask_mysqldb import MySQL
from datetime import datetime, timedelta, time
from flask import jsonify
from pytz import timezone
from passlib.hash import sha256_crypt
from collections import defaultdict
from functools import wraps
from form_classes import *
import json
import random
import time

app = Flask(__name__)
app.config.from_pyfile("config.py")



# Check if user logged in
def is_logged_in(f):
    '''this function checks whether user is logged in or not. Use this function as a decorator
    for example, if you don't want user to reach some functions without logging in put this function on top of the other function as a decorator. See upload funcion'''
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Lütfen giriş yapınız.', 'danger')
            return redirect(url_for('login'))
    return wrap

def special_requirement(f):
    @wraps(f)
    def wrap(*args ,**kwargs):
        try:
            username = session['username']
            # Create cursor
            cur = mysql.connection.cursor()
            # Check user
            if cur.execute("SELECT * FROM user WHERE username = %s", [username]):
                return f(*args ,**kwargs)
            else:
               flash('Lütfen giriş yapınız.')
               redirect(url_for('login'))
        except:
            flash('Lütfen giriş yapınız.')
            return redirect(url_for('login'))
    return wrap


mysql = MySQL(app)
@app.route('/login', methods=['POST','GET'])
def login():

   app.logger.info('Login function is processing')
   form = LoginForm(request.form)
   if request.method == 'POST' and form.validate():
      # Get Form Fields
      global username
      username = form.username.data
      password_candidate = form.password.data

      # Create cursor
      cur = mysql.connection.cursor()

      # Get user by username
      result = cur.execute("SELECT * FROM user WHERE username = %s", [username])
      print("dfsdfds",result)

      if result > 0:
         # Get stored hash
         data = cur.fetchone()
         password = data['user_password']

         # Compare Passwords
         if sha256_crypt.verify(password_candidate, password):
         #if check_password_hash(password_candidate, password):
            # Passed
            session['logged_in'] = True
            session['username'] = username

            app.logger.info('username "{}" logged in'.format(session['username']))
            return redirect(url_for('endorsement'))
         else:
            error = 'Yanlış Şifre!!! Lütfen şifrenizi kontrol ediniz yada "Şifremi Unuttum" linkini tıklayarak şifrenizi yenileyiniz.'
            return render_template('login.html', error=error, form=form)
            # Close connection
            cur.close()
      else:
         app.logger.info('Kullanıcı Adı: "%s" bulunamadı.', username)
         error = 'Kullanıcı adı bulunamadı!'
         return render_template('login.html', error=error, form=form)
   return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        company_name = form.company_name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        #password = generate_password_hash((form.password.data))
        cur = mysql.connection.cursor()
        cur.execute("select email from user")
        emails = cur.fetchall()

        dd = defaultdict(list)

        for d in (emails):
            for k, v in d.items():
                dd[k].append(v)

        if email in dd['email']:
            flash('E-mail adresiniz kayıtlı. Lütfen giriş yapınız.', 'warning')
            app.logger.info('email {} is previously registered. User returned to the login page without any change'.format(email))
            return render_template('login.html', form=form)

        cur.execute("select username from user")
        users = cur.fetchall()
        dd1 = defaultdict(list)

        for d in (users):
            for k, v in d.items():
                dd1[k].append(v)


        if username in dd1['username']:
            app.logger.info('username "{}" is previously registered. User returned to the login page without any change'.format(username))
            flash('Kullanıcı adı mevcut, lütfen giriş yapınız ya da farklı bir kullanıcı adı seçiniz.', 'warning')
            return render_template('login.html', form=form)


        # Execute query
        cur.execute("INSERT INTO user(company_name, email, username, user_password) VALUES(%s, %s, %s, %s)", (company_name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()
        app.logger.info(' {} has been registered as "{}" using email {}. User returned to the login page'.format(company_name, username, email))
        flash('Üye Oldunuz . Giriş yapabilirsiniz.', 'success')
        return render_template('login.html', form=form)
    return render_template('signup.html', form=form)

# Logout
@app.route('/logout')
@is_logged_in
def logout():

    session.clear()

    flash('Çıkış Yaptınız.', 'danger')
    return redirect(url_for('login'))

@app.route('/')
@is_logged_in
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
@is_logged_in
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
@is_logged_in
def endorsement():
   
   date_time_str = datetime.today().strftime('%Y-%m-%d') 
   date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d' )
   to_date_default = date_time_obj.date().strftime('%Y-%m-%d')
   from_date_default = (date_time_obj.date() - timedelta(days=3)).strftime('%Y-%m-%d')

   
   
   if (request.method == 'POST' ):
      
      if 'specific_Search' in request.form:
         specific_search = request.form['specific_Search']
         if specific_search == "1 Günlük":
            specific_search = 1
         elif specific_search == "1 Haftalık":
            specific_search =7
         elif specific_search == "15 Günlük":
            specific_search =15
         elif specific_search == "1 Aylık":
            specific_search =30
         elif specific_search == "3 Aylık":
            specific_search =91
         elif specific_search == "6 Aylık":
            specific_search =182
         elif specific_search == "1 Yıllık":
            specific_search =365
         
         date_time_str = datetime.now(timezone('UTC')).strftime('%Y-%m-%d')
         date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d' )
         to_date_default = date_time_obj.date().strftime('%Y-%m-%d')
         from_date = (date_time_obj.date() - timedelta(days=specific_search-1)).strftime('%Y-%m-%d')
         
         to_date = to_date_default
      else:
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
      total_income = total_income + float(i["income_price"])

   #Total expense
   total_expense = 0
   for i in expense_list:
      total_expense = total_expense + float(i["expense_price"])

   price_datas = { "total_income" : total_income,
                  "total_expense" : total_expense,
                  "diff"  : total_income-total_expense,
                  "time_period" : from_date +","+ to_date}

   print(price_datas)


   mysql.connection.commit()
   cur.close()


   return render_template("endorsement.html", **locals())


@app.route('/chart')
def index():
    return render_template('chart.html')

@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)
            print(json_data)

    return Response(generate_random_data(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

