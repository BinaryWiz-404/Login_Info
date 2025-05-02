from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'login_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return "Database connected successfully!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, password))
        mysql.connection.commit()
        cur.close()
        flash("Registration successful!", "success")
        return redirect('/')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
