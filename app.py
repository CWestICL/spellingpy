from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db = SQLAlchemy(app)

vowels = "aeiou"
consonants = "bcdfghjklmnpqrstvwxyz"

def get_char(category):
    return random.choice(category)

def get_letters():
    letters = ""
    for x in range(5):
        char = get_char(vowels)
        letters += char
    for x in range(6):
        char = get_char(consonants)
        letters += char
    for x in range(5):
        category = random.choice([vowels,consonants])
        char = get_char(category)
        letters += char
    shuffled = ''.join(random.sample(letters,len(letters)))
    print(letters)
    print(shuffled)
    return shuffled.upper()

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    word = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Score %r>" % self.id

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/daily")
def daily():
    return render_template("daily.html")

@app.route("/free")
def free():
    letters = get_letters()
    return render_template("free.html", letters=letters)

if __name__ == "__main__":
    app.run(debug=True)

"""
@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Score(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error"
    else:
        tasks = Score.query.order_by(Score.date_created).all()
        return render_template("index.html", tasks=tasks)
"""