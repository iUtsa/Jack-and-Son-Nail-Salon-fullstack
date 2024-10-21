from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="Utsa DBS",
    user="root",
    password="Utsh@das2001",
    database="Customer_and_Employee_and client_Information"
)


@app.route('/')
def home():
    return render_template('client/index.html')

@app.route('/about')
def about():
    return render_template('client/about.html')

@app.route('/services')
def services():
    return render_template('client/services.html')

@app.route('/login')
def login():
    return render_template('client/login.html')

@app.route('/nailcare')
def nailcare():
    return render_template('client/nailcare.html')

@app.route('/contact')
def contact():
    return render_template('client/contact.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)