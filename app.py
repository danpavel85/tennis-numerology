from flask import Flask, render_template, request
import datetime
import re
import os

app = Flask(__name__)

# ---------------- NUMEROLOGY CORE ----------------

letter_values = {
'A':1,'J':1,'S':1,
'B':2,'K':2,'T':2,
'C':3,'L':3,'U':3,
'D':4,'M':4,'V':4,
'E':5,'N':5,'W':5,
'F':6,'O':6,'X':6,
'G':7,'P':7,'Y':7,
'H':8,'Q':8,'Z':8,
'I':9,'R':9
}

def reduce_number(n):

    while n > 9 and n not in [11,22,33]:

        n=sum(int(d) for d in str(n))

    return n


def name_number(name):

    total=0

    for c in name.upper():

        if c in letter_values:

            total+=letter_values[c]

    return reduce_number(total)


def destiny_number(date):

    digits=[int(d) for d in re.sub(r'\D','',date)]

    return reduce_number(sum(digits))


def soul_number(name):

    vowels="AEIOU"

    total=0

    for c in name.upper():

        if c in vowels and c in letter_values:

            total+=letter_values[c]

    return reduce_number(total)


def personality_number(name):

    vowels="AEIOU"

    total=0

    for c in name.upper():

        if c not in vowels and c in letter_values:

            total+=letter_values[c]

    return reduce_number(total)


def compatibility(a,b):

    diff=abs(a-b)

    return max(0,100-diff*12)

# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template("home.html")


# ---------------- TENIS ----------------

@app.route("/tenis", methods=["GET","POST"])
def tenis():

    result=None

    if request.method=="POST":

        player1=request.form.get("player1")
        player2=request.form.get("player2")

        birth1=request.form.get("birth1")
        birth2=request.form.get("birth2")

        destiny1=destiny_number(birth1)
        destiny2=destiny_number(birth2)

        name1=name_number(player1)
        name2=name_number(player2)

        score1=compatibility(destiny1,name2)
        score2=compatibility(destiny2,name1)

        prob1=round(score1/(score1+score2)*100)
        prob2=round(score2/(score1+score2)*100)

        prediction=player1 if prob1>prob2 else player2

        result={

        "player1":player1,
        "player2":player2,

        "prob1":prob1,
        "prob2":prob2,

        "prediction":prediction

        }

    return render_template("index.html",result=result)


# ---------------- RELATIE ----------------

@app.route("/relatie", methods=["GET","POST"])
def relatie():

    result=None

    if request.method=="POST":

        name1=request.form.get("name1")
        name2=request.form.get("name2")

        birth1=request.form.get("birth1")
        birth2=request.form.get("birth2")

        destiny1=destiny_number(birth1)
        destiny2=destiny_number(birth2)

        name_num1=name_number(name1)
        name_num2=name_number(name2)

        soul1=soul_number(name1)
        soul2=soul_number(name2)

        pers1=personality_number(name1)
        pers2=personality_number(name2)

        relation_number=reduce_number(destiny1+destiny2)

        couple_energy=reduce_number(name_num1+name_num2)

        emotional=compatibility(soul1,soul2)
        sexual=compatibility(pers1,pers2)
        mental=compatibility(name_num1,name_num2)
        spiritual=compatibility(destiny1,destiny2)

        score=round((emotional+sexual+mental+spiritual)/4)

        result={

        "score":score,

        "destiny1":destiny1,
        "destiny2":destiny2,

        "name_num1":name_num1,
        "name_num2":name_num2,

        "soul1":soul1,
        "soul2":soul2,

        "pers1":pers1,
        "pers2":pers2,

        "relation_number":relation_number,
        "couple_energy":couple_energy

        }

    return render_template("relatie.html",result=result)


# ---------------- PROFIL NUMEROLOGIC ----------------

@app.route("/profil", methods=["GET","POST"])
def profil():

    result=None

    if request.method=="POST":

        name=request.form.get("name")
        birth=request.form.get("birth")

        destiny=destiny_number(birth)
        expression=name_number(name)
        soul=soul_number(name)
        personality=personality_number(name)

        maturity=reduce_number(destiny+expression)

        year=datetime.datetime.now().year

        personal_year=reduce_number(destiny+year)

        forecast=[]

        for i in range(1,10):

            forecast.append((year+i,reduce_number(personal_year+i)))

        result={

        "name":name,

        "destiny":destiny,
        "expression":expression,
        "soul":soul,
        "personality":personality,
        "maturity":maturity,

        "personal_year":personal_year,

        "forecast":forecast

        }

    return render_template("profil.html",result=result)


# ---------------- SERVER ----------------

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)