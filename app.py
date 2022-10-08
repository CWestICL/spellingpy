from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

import random
#import requests
#import aiohttp


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
db = SQLAlchemy(app)

dictionary = open('dictionary.txt', 'r')
#dictionary = open('/home/CWestICL/spellingpy/dictionary.txt', 'r')
word_list = dictionary.read().split("\n")


challenges = [
    "ehdoaopidaenarid",
    "cetayefoerouexdi",
    "efrosdoutogcfeas",
    "cedsbneeenuaaqio",
    "uppuegauutwdndvr",
    "nsnuienwaqnadlee",
    "oogatjnyrnatsiou",
    "tineieqcssovsnie",
    "qamesebahexosmgd",
    "rltliaaremaeeuse",
    "dicbopqeanueaflr",
    "wqnceteeioxraeod",
    "itduoiaetaarenbi",
    "zsiieuiaerfvtiin",
    "raydeeederieldmr",
    "eaysueetjcreiamo",
    "tuorsaujoeroniad",
    "ivdltielbmisqsoa",
    "rhhnndoeznmelooi",
    "elesruawxegdlory",
    "anzhtypnadadaiem",
    "olteaaauranesqor",
    "booreaiasugedavr",
    "euctellooehrvlmi",
    "iniprovdeoblleni",
    "tenrddectoiaazdi",
    "tnbanweciaielvfe",
    "efrewaifteumtard",
    "fetvlmaicoitdoir",
    "onosnankredseauw",
    "xoatwsodaiaitcrw",
    "mgaealiedfeoxsoa",
    "dwiiepkshathlvfe",
    "vgdiollrtoouaaig",
    "otbmaienniredegh",
    "vgdiollrtoouaaig",
    "sytneykoiasutett",
    "stiphssokieemrot",
    "oueeonwevaondher",
    "agiulinorabliena",
    "raaosineateleple",
    "stetriufltteiipb",
    "obraeossurdauetc",
    "sooleoeaidttrern"
]


print("###-Challenge check-###")
for idx, chall in enumerate(challenges):
    if len(chall) != 16:
        print("Index:",idx,"Length:",len(chall))
print("#######################")


vowels = "aaeeeiioou"
consonants = "bbccddddffggghhjkllllmmnnnnnppqrrrrrrssssttttttvvwwxyyz"

start_date = datetime(2022, 10, 1).date()

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
    #print(letters)
    #print(shuffled)
    return shuffled


def get_matches(letters):
    matches = []
    for word in word_list:
        check = 0
        for char in word:
            if word.count(char) > letters.upper().count(char):
                check = 1
        if check == 0:
            matches.append(word)
    return matches


def get_count(matches):
    count = {}
    for x in range(16):
        num = 0
        for word in matches:
            if len(word) == x + 1:
                num += 1
        if num > 0:
            count["{}".format(x + 1)] = num
    return count



def check_word(answer):
    print("Checking dictionary...")

    """
    app_id = '6ce7ceb9'
    app_key = 'bac47f553632715817395f753efc74d2'
    language = 'en-gb'
    word_id = answer

    url = 'https://od-api.oxforddictionaries.com/api/v2/lemmas/'  + language + '/'  + word_id.lower()
    r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})

    print(r.status_code)
    status = str(r.status_code)

    if status == "404":
        return 0

    elif status == "200":
        return len(word_id)

    else:
        raise aiohttp.ClientError("Dictionary server failed to respond correctly")
    """
    if answer in word_list:
        return len(answer)
    else:
        return 0

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    word = db.Column(db.String(16), nullable=False)
    challenge = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        score_dic = {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "word": self.word,
            "challenge": self.challenge,
            "date": self.date_created.strftime("%Y/%m/%d")
        }
        return str(score_dic)


@app.route("/")
def index():
    return redirect("/daily")


@app.route("/daily")
def daily():
    return render_template("daily.html")


@app.route("/free")
def free():
    return render_template("free.html")
    #return redirect("/daily")


@app.route("/scores", methods=["POST","GET"])
def post_score():
    if request.method == "POST":
        if request.is_json:
            req = request.get_json()
            print(type(req))
            print(req)

            try:
                name = req["name"]
                answer = req["word"]
                score = check_word(answer)
                chall_num = req["challenge"]

                new_score = Score(name=name, score=score, word=answer, challenge=chall_num)
                db.session.add(new_score)
                db.session.commit()

                response = {
                    "message": "Score submitted",
                    "word": answer,
                    "score": score
                }
                res = make_response(jsonify(response), 200)
                return res

            except Exception as e:
                print(e)
                response = {
                    "message": "There was an error submitting score"
                }
                res = make_response(jsonify(response), 400)
                return res

        else:
            response = {
                "message": "JSON not received"
            }
            res = make_response(jsonify(response), 400)
            return res

    else:
        print("Score GET")
        scores = Score.query.order_by(Score.id).all()
        print(scores)
        print(type(scores))

        res = make_response(jsonify(str(scores)), 200)
        return res


@app.route("/scores/check", methods=["POST"])
def check_score():
    if request.is_json:
        req = request.get_json()
        print(type(req))
        print(req)

        try:
            answer = req["word"]
            score = check_word(answer)

            response = {
                "message": "Score checked",
                "word": answer,
                "score": score
            }
            res = make_response(jsonify(response), 200)
            return res

        except Exception as e:
            print(e)
            response = {
                "message": "There was an error submitting score"
            }
            res = make_response(jsonify(response), 400)
            return res

    else:
        response = {
            "message": "JSON not received"
        }
        res = make_response(jsonify(response), 400)
        return res


@app.route("/scores/<int:id>", methods=["GET","PUT","DELETE"])
def delete(id):
    if request.method == "DELETE":
        score_delete = Score.query.get_or_404(id)
        print("Deleting score with ID: " + str(id))

        try:
            db.session.delete(score_delete)
            db.session.commit()

            response = {
                "message": "Score ID: " + str(id) + " has been deleted"
            }
            res = make_response(jsonify(response), 200)
            return res

        except Exception as e:
            print(e)
            response = {
                "message": "There was an error deleting score"
            }
            res = make_response(jsonify(response), 400)
            return res

    elif request.method == "PUT":
        score_update = Score.query.get_or_404(id)
        print("Updating score with ID: " + str(id))
        print(score_update)

        if request.is_json:
            req = request.get_json()
            print(type(req))
            print(req)

            try:
                if "name" in req:
                    score_update.name = req["name"]

                if "score" in req:
                    score_update.score = req["score"]

                if "word" in req:
                    score_update.word = req["word"]

                if "challenge" in req:
                    score_update.challenge = req["challenge"]

                print(score_update)
                db.session.commit()

                response = {
                    "message": "Score ID: " + str(id) + " has been updated"
                }
                res = make_response(jsonify(response), 200)
                return res

            except Exception as e:
                print(e)
                response = {
                    "message": "There was an error updating score"
                }
                res = make_response(jsonify(response), 400)
                return res

        else:
            response = {
                "message": "JSON not received"
            }
            res = make_response(jsonify(response), 400)
            return res

    else:
        scores = Score.query.order_by(Score.score).filter(Score.challenge == (id)).all()
        print(scores)
        print(type(scores))

        res = make_response(jsonify(str(scores)), 200)
        return res


@app.route("/boards", methods=["GET","POST"])
def board():
    if request.method == "POST":
        answer = request.form["word"]
        score = request.form["score"]
        chall = request.form["challenge"]

        if int(score) > 0:
            message = "You scored " + score + " with the word " + answer + "!"

        else:
            message = "Sorry, " + answer + " wasn't in the word list. You scored 0."

        return render_template("daily-board.html", message=message, chall=chall)

    else:
        return render_template("board.html")


@app.route("/challenges")
def challenge():
    today_date = datetime.utcnow().date()
    time = datetime.utcnow()
    challenge_day = (today_date - start_date).days
    today_challenge = challenges[challenge_day]

    response = {
        "start": start_date,
        "today": today_date,
        "time": time,
        "daysbetween": challenge_day,
        "challenge": today_challenge,
        "number": challenge_day + 1,
        "total": len(challenges)
    }
    res = make_response(jsonify(response), 200)
    return res


@app.route("/challenges/<int:id>")
def challenge_id(id):
    response = {
        "challenge": challenges[id - 1],
        "date": (start_date + timedelta(days=id - 1)).strftime("%Y/%m/%d")
    }
    res = make_response(jsonify(response), 200)
    return res


@app.route("/letters")
def rand_letters():
    letters = get_letters()
    matches = get_matches(letters)
    count = get_count(matches)
    response = {
        "letters": letters,
        "matches": sorted(matches, key=len, reverse=True),
        "count" : count
    }
    res = make_response(jsonify(response), 200)
    return res


@app.route("/letters/<let>")
def check_letters(let):
    letters = let
    matches = get_matches(letters)
    count = get_count(matches)
    response = {
        "letters": letters,
        "matches": sorted(matches, key=len, reverse=True),
        "count" : count
    }
    res = make_response(jsonify(response), 200)
    return res

"""
@app.route("/dictionary")
def dict():
    response = {
        "words": word_list
    }
    res = make_response(jsonify(response), 200)
    return res
"""


if __name__ == "__main__":
    app.run(debug=True)