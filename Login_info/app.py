from flask import Flask, render_template, request, redirect, flash,session, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = 'myflaskloginappsecretkey123'  # Needed for flash messages

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'login_db'

mysql = MySQL(app)

# @app.route('/')
# def home_page():
#     return "Database connected successfully!"
@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password=generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        session['username'] = username  # Automatically log in the user after registration
        flash("Registration successful!", "success")
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s ", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for('register'))

    return render_template('login.html')


    
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
