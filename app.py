import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

app.secret_key = 'secret123'

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT"))
)

@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/booking') 
def booking():
    return render_template('booking.html')

@app.route('/mybooking')
def mybooking():
    return render_template('my_booking.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate inputs
        if not username or not email or not password:
            flash("All fields are required", "danger")
            return render_template("signup.html")
        
        hashed_pw = generate_password_hash(password)

        try:
            cursor = db.cursor()
            
            query = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
            values = (username, email, hashed_pw, 'guest')
            
            cursor.execute(query, values)
            db.commit()
            
            flash("Account created successfully!", "success")
            return redirect(url_for('login'))
            
        except mysql.connector.IntegrityError as err:
            if "Duplicate entry" in str(err):
                flash("Username or email already exists", "danger")
            else:
                flash("Error creating account", "danger")
        except mysql.connector.Error as err:
            flash("Database error occurred", "danger")
            print(f"DEBUG SQL ERROR: {err}")
        finally:
            if cursor:
                cursor.close()

    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            if db:
                cursor = db.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user and check_password_hash(user['password_hash'], password):
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    return redirect(url_for('home'))
                else:
                    flash("Invalid credentials", "danger")
        except mysql.connector.Error as err:
            flash(f"Connection error: {err}", "danger")
            
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5010, debug=True)
        