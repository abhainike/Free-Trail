from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os

JASPER_AI_URL = "https://jasper.ai/free-trial?fpr=freedemo"
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Costumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.first_name + " " + self.last_name


@app.route('/')
def home():
    user_details = str(request.user_agent)
    if "Windows" in user_details or "Macintosh" in user_details:
        is_pc = True
    else:
        is_pc = False
    return render_template('index.html', is_pc=is_pc)


@app.route('/email', methods = ['POST', 'GET'])
def register():

    if request.method == "POST":

        email = request.form['email']
        email_exist = Costumer.query.filter_by(email=email).first()
        
        if email_exist:
            flash("Email already exist")
            return redirect(url_for('register'))
        
        last_name = request.form['last_name']
        first_name = request.form['first_name']
        new_costumer = Costumer(email = email, last_name=last_name, first_name=first_name)
        db.session.add(new_costumer)
        db.session.commit()
        return redirect(JASPER_AI_URL)

    return render_template("register.html")

app.run(debug=True)