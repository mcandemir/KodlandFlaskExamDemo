# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, session
import MySQLdb

app = Flask(__name__)
app.secret_key = "c00lsw4gk3y"

NUM_QUESTIONS = 4


def get_user_answers(form_dict):
    # create dict
    user_answers = {}
    for i in range(1, NUM_QUESTIONS + 1):
        user_answers[f"q{i}"] = ""

    # get answers
    for i in range(1, NUM_QUESTIONS + 1):
        if f"question{i}" in form_dict:
            user_answers[f"q{i}"] = form_dict[f"question{i}"]
    return user_answers


def calculate_score(user_answers, ground_answers):
    num_answered_true = 0
    for i in range(1, NUM_QUESTIONS + 1):
        if user_answers[f"q{i}"] == ground_answers[f"q{i}"]:
            num_answered_true += 1
    return (num_answered_true / NUM_QUESTIONS) * 100


@app.route("/", methods=["GET", "POST"])
def exam():
    if request.method == "GET":
        session["bestscore"] = 0
        score = 0
        return render_template(
            "index.html", score=score, bestscore=session["bestscore"]
        )

    elif request.method == "POST":
        db = MySQLdb.Connect(
            host="mcandemir.mysql.pythonanywhere-services.com",
            user="mcandemir",
            password="Can12301230*",
            database="mcandemir$default",
        )

        # get from database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Answers")

        # COLS: ((examid, q1, q2, q3, q4),)
        ground = cursor.fetchall()
        q1, q2, q3, q4 = ground[0][1], ground[0][2], ground[0][3], ground[0][4]
        ground_answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4}

        # get user answers
        user_answers = get_user_answers(request.form)

        # calc score
        score = calculate_score(user_answers, ground_answers)

        # update best score
        if score > session["bestscore"]:
            session["bestscore"] = score

    return render_template("index.html", score=score, bestscore=session["bestscore"])
