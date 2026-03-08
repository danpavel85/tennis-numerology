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


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- TENIS ----------------

@app.route("/tenis", methods=["GET","POST"])
def tenis():

    result=None

    if request.method=="POST":

        p1=request.form["player1"]
        p2=request.form["player2"]

        b1=request.form["birth1"]
        b2=request.form["birth2"]

        destiny1=destiny_number(b1)
        destiny2=destiny_number(b2)

        name1=name_number(p1)
        name2=name_number(p2)

        score1=compatibility(destiny1,name2)
        score2=compatibility(destiny2,name1)

        if score1+score2==0:
            prob1=50
            prob2=50
        else:
            prob1=round(score1/(score1+score2)*100)
            prob2=round(score2/(score1+score2)*100)

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

        name1=request.form["name1"]
        married1=request.form.get("married1","")

        birth1=request.form["birth1"]
        time1=request.form.get("time1","")
        place1=request.form.get("place1","")


        name2=request.form["name2"]
        married2=request.form.get("married2","")

        birth2=request.form["birth2"]
        time2=request.form.get("time2","")
        place2=request.form.get("place2","")


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


if __name__=="__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)