from flask import Flask, render_template, request
import re
import datetime

app = Flask(__name__)


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

    total=0

    for c in name.upper():
        if c in letter_values:
            total+=letter_values[c]

    return reduce_number(total)


def destiny_number(date):

    digits=[int(d) for d in re.sub(r'\D','',date)]

    return reduce_number(sum(digits))


def universal_day(date):

    digits=[int(d) for d in re.sub(r'\D','',date)]

    return reduce_number(sum(digits))


def personal_day(birth,match):

    b=sum(int(d) for d in re.sub(r'\D','',birth))
    m=sum(int(d) for d in re.sub(r'\D','',match))

    return reduce_number(b+m)


def personal_year(birth,match):

    birth_digits=[int(d) for d in re.sub(r'\D','',birth)][4:]
    year_digits=[int(d) for d in match[:4]]

    return reduce_number(sum(birth_digits)+sum(year_digits))


def hour_vibration(time):

    digits=[int(d) for d in re.sub(r'\D','',time)]

    return reduce_number(sum(digits))


def word_vibration(word):

    total=0

    for c in word.upper():
        if c in letter_values:
            total+=letter_values[c]

    return reduce_number(total)


def compatibility_score(a,b):

    diff=abs(a-b)

    return max(0,100-diff*10)


# -----------------------------
# PAGINA ANALIZA TENIS
# -----------------------------

@app.route("/", methods=["GET","POST"])
def index():

    result=None

    if request.method=="POST":

        p1=request.form["player1"]
        b1=request.form["birth1"]

        p2=request.form["player2"]
        b2=request.form["birth2"]

        date=request.form["date"]
        time=request.form["time"]
        surface=request.form["surface"]
        round_name=request.form["round"]
        tournament=request.form["tournament"]

        odds1=request.form.get("odds1")
        odds2=request.form.get("odds2")

        day=universal_day(date)
        hour=hour_vibration(time)
        surface_v=word_vibration(surface)
        round_v=word_vibration(round_name)
        location_v=word_vibration(tournament)

        event_total=reduce_number(day+hour+surface_v+round_v+location_v)

        destiny1=destiny_number(b1)
        destiny2=destiny_number(b2)

        name1=name_number(p1)
        name2=name_number(p2)

        personal1=personal_day(b1,date)
        personal2=personal_day(b2,date)

        year1=personal_year(b1,date)
        year2=personal_year(b2,date)

        score1=compatibility_score(destiny1,event_total)
        score2=compatibility_score(destiny2,event_total)

        total_score=score1+score2

        if total_score==0:
            prob1=50
            prob2=50
        else:
            prob1=round((score1/total_score)*100)
            prob2=round((score2/total_score)*100)

        prediction=p1 if prob1>prob2 else p2

        book_prob1=None
        book_prob2=None
        value1=None
        value2=None

        if odds1 and odds2:

            odds1=float(odds1)
            odds2=float(odds2)

            book_prob1=round((1/odds1)*100,2)
            book_prob2=round((1/odds2)*100,2)

            value1=round(prob1-book_prob1,2)
            value2=round(prob2-book_prob2,2)

        result={

        "player1":p1,
        "player2":p2,

        "day":day,
        "hour":hour,
        "surface":surface_v,
        "round":round_v,
        "location":location_v,
        "event":event_total,

        "p1":{
            "destiny":destiny1,
            "name":name1,
            "personal":personal1,
            "year":year1
        },

        "p2":{
            "destiny":destiny2,
            "name":name2,
            "personal":personal2,
            "year":year2
        },

        "prob1":prob1,
        "prob2":prob2,

        "book_prob1":book_prob1,
        "book_prob2":book_prob2,

        "value1":value1,
        "value2":value2,

        "prediction":prediction

        }

    return render_template("index.html",result=result)



# -----------------------------
# PAGINA COMPATIBILITATE RELATIE
# -----------------------------

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


def couple_vibration(n1,n2):

    return reduce_number(name_number(n1)+name_number(n2))


def relationship_years(date):

    years=[]

    if date:

        start=int(date[:4])
        current=datetime.datetime.now().year

        for y in range(current,current+5):

            vib=reduce_number(start+y)

            years.append((y,vib))

    return years


@app.route("/relatie", methods=["GET","POST"])
def relatie():

    result=None

    if request.method=="POST":

        name1=request.form["name1"]
        name2=request.form["name2"]

        birth1=request.form["birth1"]
        birth2=request.form["birth2"]

        relation_date=request.form.get("relation_date","")

        destiny1=destiny_number(birth1)
        destiny2=destiny_number(birth2)

        soul1=soul_number(name1)
        soul2=soul_number(name2)

        pers1=personality_number(name1)
        pers2=personality_number(name2)

        relation_number=reduce_number(destiny1+destiny2)

        couple_energy=couple_vibration(name1,name2)

        emotional=compatibility_score(soul1,soul2)

        sexual=compatibility_score(pers1,pers2)

        score=round((emotional+sexual)/2)

        marriage=min(100,score+10 if relation_number in [2,6] else score)

        divorce=max(0,100-score)

        karmic="Relatie karmica" if destiny1==destiny2 else "Relatie normala"

        years=relationship_years(relation_date)

        result={

        "name1":name1,
        "name2":name2,

        "destiny1":destiny1,
        "destiny2":destiny2,

        "soul1":soul1,
        "soul2":soul2,

        "relation_number":relation_number,

        "couple_energy":couple_energy,

        "emotional":emotional,
        "sexual":sexual,

        "score":score,

        "karmic":karmic,

        "marriage":marriage,
        "divorce":divorce,

        "years":years

        }

    return render_template("relatie.html",result=result)


if __name__=="__main__":
    app.run(debug=True)