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


def destiny_number(date):
    digits = [int(d) for d in re.sub(r'\D','',date)]
    return reduce_number(sum(digits))


def name_number(name):

    total = 0

    for c in name.upper():
        if c in letter_values:
            total += letter_values[c]

    return reduce_number(total)


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


def couple_vibration(name1,name2):

    return reduce_number(name_number(name1)+name_number(name2))


def emotional_compatibility(s1,s2):

    diff=abs(s1-s2)

    return max(0,100-diff*12)


def sexual_compatibility(p1,p2):

    diff=abs(p1-p2)

    return max(0,100-diff*10)


def karmic_analysis(d1,d2,s1,s2):

    if d1==d2 and s1==s2:
        return "Relatie karmica foarte puternica"

    if d1==d2:
        return "Relatie karmica"

    if abs(d1-d2)==1:
        return "Relatie de lectie karmica"

    return "Relatie normala"


def marriage_probability(score,relation):

    base=score

    if relation in [2,6]:
        base+=10

    return min(100,base)


def divorce_probability(score):

    return max(0,100-score)


def relationship_years(relation_date):

    years=[]

    if relation_date:

        year=int(relation_date[:4])

        current=datetime.datetime.now().year

        for y in range(current,current+5):

            vib=reduce_number(y+year)

            years.append((y,vib))

    return years


@app.route("/relatie", methods=["GET","POST"])
def relatie():

    result=None

    if request.method=="POST":

        name1=request.form["name1"]
        married1=request.form.get("married1","")
        birth1=request.form["birth1"]

        name2=request.form["name2"]
        married2=request.form.get("married2","")
        birth2=request.form["birth2"]

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

        couple_energy=couple_vibration(name1,name2)


        emotional=emotional_compatibility(soul1,soul2)

        sexual=sexual_compatibility(pers1,pers2)

        score=round((emotional+sexual)/2)


        karmic=karmic_analysis(destiny1,destiny2,soul1,soul2)

        marriage=marriage_probability(score,relation_number)

        divorce=divorce_probability(score)

        years=relationship_years(relation_date)


        result={

        "name1":name1,
        "name2":name2,

        "destiny1":destiny1,
        "destiny2":destiny2,

        "name_num1":name_num1,
        "name_num2":name_num2,

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