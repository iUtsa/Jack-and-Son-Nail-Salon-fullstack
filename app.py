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
#type code below do not adjust the information above

#def create_account():
   # if



if __name__ == "__main__":
    app.run(debug=True)