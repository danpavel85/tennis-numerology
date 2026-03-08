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
    digits = [int(d) for d in re.sub(r'\D', '', date)]
    return reduce_number(sum(digits))


def compatibility(a, b):
    diff = abs(a - b)
    return max(0, 100 - diff * 12)


def text_vibration(text):
    if not text:
        return 0
    total = 0
    for c in text.upper():
        if c in letter_values:
            total += letter_values[c]
    return reduce_number(total)


def date_vibration(date):
    digits = [int(d) for d in re.sub(r'\D', '', date)]
    return reduce_number(sum(digits))


def time_vibration(time):
    if not time:
        return 0
    digits = [int(d) for d in re.sub(r'\D', '', time)]
    return reduce_number(sum(digits))


def year_energy(birthdate):
    year = datetime.datetime.now().year
    digits = [int(d) for d in re.sub(r'\D', '', birthdate + str(year))]
    return reduce_number(sum(digits))


def personal_day(birthdate, matchdate):
    digits = [int(d) for d in re.sub(r'\D', '', birthdate + matchdate)]
    return reduce_number(sum(digits))


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- TENIS ----------------

@app.route("/tenis", methods=["GET","POST"])
def tenis():

    result=None

    if request.method=="POST":

        player1=request.form.get("player1","")
        player2=request.form.get("player2","")

        birth1=request.form.get("birth1","")
        birth2=request.form.get("birth2","")

        odds1=request.form.get("odds1")
        odds2=request.form.get("odds2")

        date=request.form.get("date","")
        time=request.form.get("time","")
        tournament=request.form.get("tournament","")

        surface=request.form.get("surface","")
        round_name=request.form.get("round","")

        # ----- energia meciului -----

        day_vib=date_vibration(date)
        hour_vib=time_vibration(time)
        location_vib=text_vibration(tournament)
        surface_vib=text_vibration(surface)
        round_vib=text_vibration(round_name)

        event_energy=reduce_number(
            day_vib+hour_vib+location_vib+surface_vib+round_vib
        )

        pressure=reduce_number(surface_vib+round_vib)

        # ----- jucator 1 -----

        p1_destiny=destiny_number(birth1)
        p1_name=name_number(player1)
        p1_year=year_energy(birth1)
        p1_personal=personal_day(birth1,date)

        p1_score=compatibility(p1_destiny,event_energy)

        # ----- jucator 2 -----

        p2_destiny=destiny_number(birth2)
        p2_name=name_number(player2)
        p2_year=year_energy(birth2)
        p2_personal=personal_day(birth2,date)

        p2_score=compatibility(p2_destiny,event_energy)

        # ----- probabilitate numerologica -----

        total=p1_score+p2_score

        prob1=round(p1_score/total*100)
        prob2=round(p2_score/total*100)

        prediction=player1 if prob1>prob2 else player2

        # ----- bookmaker -----

        book_prob1=None
        book_prob2=None
        value1=None
        value2=None

        if odds1 and odds2:

            odds1=float(odds1)
            odds2=float(odds2)

            book_prob1=round(100/odds1,2)
            book_prob2=round(100/odds2,2)

            value1=round(prob1-book_prob1,2)
            value2=round(prob2-book_prob2,2)

        result={

            "player1":player1,
            "player2":player2,

            "day":day_vib,
            "hour":hour_vib,
            "location":location_vib,
            "surface":surface_vib,
            "round":round_vib,
            "event":event_energy,
            "pressure":pressure,

            "p1":{
                "destiny":p1_destiny,
                "name":p1_name,
                "year":p1_year,
                "personal":p1_personal,
                "score":p1_score
            },

            "p2":{
                "destiny":p2_destiny,
                "name":p2_name,
                "year":p2_year,
                "personal":p2_personal,
                "score":p2_score
            },

            "prob1":prob1,
            "prob2":prob2,

            "prediction":prediction,

            "book_prob1":book_prob1,
            "book_prob2":book_prob2,

            "value1":value1,
            "value2":value2

        }

    return render_template("index.html",result=result)


# ---------------- RELATIE ----------------

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


def relationship_years(date):

    years=[]

    if date:

        start=int(date[:4])
        current=datetime.datetime.now().year

        for y in range(current,current+5):
            vib=reduce_number(start+y)
            years.append((y,vib))

    return years


def interpretation(score):

    if score>85:
        return "Compatibilitate extrem de puternica."

    if score>70:
        return "Compatibilitate foarte buna."

    if score>50:
        return "Compatibilitate moderata."

    return "Compatibilitate scazuta."


@app.route("/relatie", methods=["GET","POST"])
def relatie():

    result=None

    if request.method=="POST":

        name1=request.form.get("name1","")
        name2=request.form.get("name2","")

        birth1=request.form.get("birth1","")
        birth2=request.form.get("birth2","")

        relation_date=request.form.get("relation_date","")

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

        communication=compatibility(name_num1,soul2)
        trust=compatibility(destiny1,soul1)
        passion=compatibility(pers1,pers2)
        stability=compatibility(destiny1,name_num2)

        friendship=compatibility(soul1,name_num2)
        values_score=compatibility(destiny1,destiny2)
        lifestyle=compatibility(pers1,name_num2)
        attraction=compatibility(pers1,soul2)

        compat_list=[
            emotional,sexual,mental,spiritual,
            communication,trust,passion,stability,
            friendship,values_score,lifestyle,attraction
        ]

        score=round(sum(compat_list)/len(compat_list))

        marriage=min(100,score+10 if relation_number in [2,6] else score)
        divorce=max(0,100-score)

        karmic="Relatie karmica" if destiny1==destiny2 else "Relatie normala"

        years=relationship_years(relation_date)

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
            "couple_energy":couple_energy,

            "emotional":emotional,
            "sexual":sexual,
            "mental":mental,
            "spiritual":spiritual,

            "communication":communication,
            "trust":trust,
            "passion":passion,
            "stability":stability,

            "friendship":friendship,
            "values_score":values_score,
            "lifestyle":lifestyle,
            "attraction":attraction,

            "marriage":marriage,
            "divorce":divorce,

            "karmic":karmic,
            "interpretation":interpretation(score),

            "years":years
        }

    return render_template("relatie.html",result=result)


# ---------------- RUN SERVER ----------------

if __name__=="__main__":

    port=int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0",port=port)