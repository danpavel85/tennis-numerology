from flask import Flask, render_template, request
import datetime
import re
import os

app = Flask(__name__)

# ---------------- NUMEROLOGY ----------------

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
        n = sum(int(d) for d in str(n))
    return n

def name_number(name):
    total = 0
    for c in name.upper():
        if c in letter_values:
            total += letter_values[c]
    return reduce_number(total)

def destiny_number(date):
    digits = [int(d) for d in re.sub(r'\D','',date)]
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

        p1=request.form.get("player1")
        p2=request.form.get("player2")

        b1=request.form.get("birth1")
        b2=request.form.get("birth2")

        d1=destiny_number(b1)
        d2=destiny_number(b2)

        n1=name_number(p1)
        n2=name_number(p2)

        s1=compatibility(d1,n2)
        s2=compatibility(d2,n1)

        total = s1 + s2

        if total == 0:
            prob1 = 50
            prob2 = 50
        else:
            prob1 = round(s1/total*100)
            prob2 = round(s2/total*100)

        prediction=p1 if prob1>prob2 else p2

        result={
            "player1":p1,
            "player2":p2,
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

        d1=destiny_number(birth1)
        d2=destiny_number(birth2)

        n1=name_number(name1)
        n2=name_number(name2)

        soul1=soul_number(name1)
        soul2=soul_number(name2)

        pers1=personality_number(name1)
        pers2=personality_number(name2)

        relation=reduce_number(d1+d2)
        couple=reduce_number(n1+n2)

        emotional=compatibility(soul1,soul2)
        sexual=compatibility(pers1,pers2)
        mental=compatibility(n1,n2)
        spiritual=compatibility(d1,d2)

        score=round((emotional+sexual+mental+spiritual)/4)

        result={
            "score":score,
            "destiny1":d1,
            "destiny2":d2,
            "name_num1":n1,
            "name_num2":n2,
            "soul1":soul1,
            "soul2":soul2,
            "pers1":pers1,
            "pers2":pers2,
            "relation_number":relation,
            "couple_energy":couple
        }

    return render_template("relatie.html",result=result)

# ---------------- PROFIL ----------------

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

        birth_digits=[int(d) for d in re.sub(r'\D','',birth)]

        life_cycle1=reduce_number(birth_digits[1])
        life_cycle2=reduce_number(birth_digits[2])
        life_cycle3=reduce_number(birth_digits[0])

        challenge1=abs(life_cycle1-life_cycle2)
        challenge2=abs(life_cycle2-life_cycle3)
        challenge3=abs(life_cycle1-life_cycle3)

        current_year=datetime.datetime.now().year

        personal_year=reduce_number(destiny+current_year)

        personal_month=reduce_number(personal_year+datetime.datetime.now().month)

        personal_day=reduce_number(personal_month+datetime.datetime.now().day)

        forecast_years=[]

        for i in range(1,10):

            year=current_year+i

            vib=reduce_number(personal_year+i)

            forecast_years.append((year,vib))

        forecast_months=[]

        for m in range(1,13):

            vib=reduce_number(personal_year+m)

            forecast_months.append((m,vib))

        karmic=[]

        if destiny in [13,14,16,19]:

            karmic.append(destiny)

        result={

        "destiny":destiny,
        "expression":expression,
        "soul":soul,
        "personality":personality,
        "maturity":maturity,

        "life_cycle1":life_cycle1,
        "life_cycle2":life_cycle2,
        "life_cycle3":life_cycle3,

        "challenge1":challenge1,
        "challenge2":challenge2,
        "challenge3":challenge3,

        "personal_year":personal_year,
        "personal_month":personal_month,
        "personal_day":personal_day,

        "forecast_years":forecast_years,
        "forecast_months":forecast_months,

        "karmic":karmic

        }

    return render_template("profil.html",result=result)

# ---------------- RUN SERVER ----------------

if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)