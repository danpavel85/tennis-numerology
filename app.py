from flask import Flask, render_template, request
import re

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

compatibility = {
1:[1,3,5,6,8],
2:[2,4,6,8],
3:[1,3,6,9],
4:[2,4,8],
5:[1,5,7],
6:[1,2,3,6,9],
7:[5,7],
8:[1,2,4,8],
9:[3,6,9]
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


def universal_day(date):
    digits = [int(d) for d in re.sub(r'\D','',date)]
    return reduce_number(sum(digits))


def personal_day(birth, match):
    b = sum(int(d) for d in re.sub(r'\D','',birth))
    m = sum(int(d) for d in re.sub(r'\D','',match))
    return reduce_number(b + m)


def personal_year(birth, match):

    birth_digits = [int(d) for d in re.sub(r'\D','',birth)][4:]
    year_digits = [int(d) for d in match[:4]]

    return reduce_number(sum(birth_digits) + sum(year_digits))


def hour_vibration(time):
    digits = [int(d) for d in re.sub(r'\D','',time)]
    return reduce_number(sum(digits))


def word_vibration(word):
    total = 0
    for c in word.upper():
        if c in letter_values:
            total += letter_values[c]
    return reduce_number(total)


def compatibility_score(player_number, event_number):

    if event_number in compatibility.get(player_number, []):
        return 2

    if player_number == event_number:
        return 3

    if abs(player_number-event_number) == 1:
        return 1

    return 0


def competition_pressure(round_name):

    pressure = {
        "Round of 128":"Presiune foarte mica",
        "Round of 64":"Presiune mica",
        "Round of 32":"Presiune moderata",
        "Round of 16":"Presiune ridicata",
        "Quarterfinal":"Presiune mare",
        "Semifinal":"Presiune foarte mare",
        "Final":"Presiune maxima"
    }

    return pressure.get(round_name,"Necunoscut")


@app.route("/", methods=["GET","POST"])
def index():

    result = None

    if request.method == "POST":

        p1 = request.form["player1"]
        b1 = request.form["birth1"]

        p2 = request.form["player2"]
        b2 = request.form["birth2"]

        date = request.form["date"]
        time = request.form["time"]
        surface = request.form["surface"]
        round_name = request.form["round"]
        tournament = request.form["tournament"]

        day = universal_day(date)
        hour = hour_vibration(time)
        surface_v = word_vibration(surface)
        round_v = word_vibration(round_name)
        location_v = word_vibration(tournament)

        event_total = reduce_number(day + hour + surface_v + round_v + location_v)

        def analyze(name,birth):

            destiny = destiny_number(birth)
            name_num = name_number(name)
            personal = personal_day(birth,date)
            year = personal_year(birth,date)

            score = 0
            score += compatibility_score(destiny,event_total)
            score += compatibility_score(name_num,event_total)
            score += compatibility_score(personal,event_total)

            return {
                "destiny":destiny,
                "name":name_num,
                "personal":personal,
                "year":year,
                "score":score
            }

        p1_data = analyze(p1,b1)
        p2_data = analyze(p2,b2)

        total_score = p1_data["score"] + p2_data["score"]

        if total_score == 0:
            prob1 = 50
            prob2 = 50
        else:
            prob1 = round((p1_data["score"] / total_score) * 100)
            prob2 = round((p2_data["score"] / total_score) * 100)

        if prob1 > prob2:
            prediction = p1
        elif prob2 > prob1:
            prediction = p2
        else:
            prediction = "Meci echilibrat"

        result = {
            "day":day,
            "hour":hour,
            "surface":surface_v,
            "round":round_v,
            "location":location_v,
            "event":event_total,
            "pressure":competition_pressure(round_name),
            "p1":p1_data,
            "p2":p2_data,
            "prob1":prob1,
            "prob2":prob2,
            "prediction":prediction,
            "player1":p1,
            "player2":p2
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)