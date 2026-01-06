from flask import Flask, render_template, request, redirect, url_for, session, make_response


app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/booking') 
def booking():
    return render_template('booking.html')

@app.route('/login') 
def login():
    return render_template('login.html')

@app.route('/signup') 
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5010, debug=True)
        