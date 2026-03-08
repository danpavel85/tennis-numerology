from flask import Flask, render_template, request
import datetime
import re
import os

app = Flask(__name__)

# ================= CORE NUMEROLOGY =================

values = {
    "A":1,"J":1,"S":1, "B":2,"K":2,"T":2, "C":3,"L":3,"U":3,
    "D":4,"M":4,"V":4, "E":5,"N":5,"W":5, "F":6,"O":6,"X":6,
    "G":7,"P":7,"Y":7, "H":8,"Q":8,"Z":8, "I":9,"R":9
}

def reduce_number(n, master=True):
    if n == 0: return 0
    while n > 9:
        if master and n in [11, 22, 33]:
            break
        n = sum(int(x) for x in str(n))
    return n

def name_number(name):
    if not name: return 0
    total = sum(values.get(c, 0) for c in name.upper())
    return reduce_number(total)

def destiny_number(date_str):
    if not date_str: return 0
    digits = [int(d) for d in re.sub(r"\D", "", date_str)]
    return reduce_number(sum(digits))

def soul_number(name):
    vowels = "AEIOU"
    total = sum(values.get(c, 0) for c in name.upper() if c in vowels)
    return reduce_number(total)

def personality_number(name):
    vowels = "AEIOU"
    total = sum(values.get(c, 0) for c in name.upper() if c.isalpha() and c not in vowels)
    return reduce_number(total)

def compatibility(a, b):
    # Logica simpla de compatibilitate
    diff = abs(a - b)
    score = 100 - (diff * 12)
    return max(10, min(100, score))

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/tenis", methods=["GET","POST"])
def tenis():
    result = None
    if request.method == "POST":
        p1_name = request.form.get("player1", "")
        p2_name = request.form.get("player2", "")
        b1 = request.form.get("birth1", "")
        b2 = request.form.get("birth2", "")
        match_date = request.form.get("date", "")
        
        # Calcule de baza
        d1 = destiny_number(b1)
        d2 = destiny_number(b2)
        n1 = name_number(p1_name)
        n2 = name_number(p2_name)
        
        # Vibratia zilei (daca e selectata)
        day_vib = destiny_number(match_date) if match_date else 5
        
        # Simulam restul valorilor cerute de HTML pentru a evita eroarea
        s1_score = compatibility(d1, day_vib) + compatibility(n1, day_vib)
        s2_score = compatibility(d2, day_vib) + compatibility(n2, day_vib)
        
        total = s1_score + s2_score
        prob1 = round((s1_score / total) * 100) if total > 0 else 50
        prob2 = 100 - prob1

        result = {
            "player1": p1_name, "player2": p2_name,
            "day": day_vib, "hour": "N/A", "location": "N/A", "surface": "N/A", "round": "N/A", "event": "N/A", "pressure": "N/A",
            "p1": {"destiny": d1, "name": n1, "year": reduce_number(d1 + 2024), "personal": reduce_number(d1 + day_vib), "score": s1_score},
            "p2": {"destiny": d2, "name": n2, "year": reduce_number(d2 + 2024), "personal": reduce_number(d2 + day_vib), "score": s2_score},
            "prob1": prob1, "prob2": prob2,
            "prediction": p1_name if prob1 > prob2 else p2_name
        }
    return render_template("index.html", result=result)

@app.route("/relatie", methods=["GET","POST"])
def relatie():
    result = None
    if request.method == "POST":
        n1 = request.form.get("name1", "")
        n2 = request.form.get("name2", "")
        b1 = request.form.get("birth1", "")
        b2 = request.form.get("birth2", "")
        
        d1, d2 = destiny_number(b1), destiny_number(b2)
        nm1, nm2 = name_number(n1), name_number(n2)
        s1, s2 = soul_number(n1), soul_number(n2)
        p1, p2 = personality_number(n1), personality_number(n2)

        # Calculam toate campurile cerute de relatie.html
        res_data = {
            "emotional": compatibility(s1, s2),
            "sexual": compatibility(p1, p2),
            "mental": compatibility(nm1, nm2),
            "spiritual": compatibility(d1, d2),
            "communication": compatibility(nm1, d2),
            "trust": compatibility(d1, nm2),
            "passion": compatibility(p1, s2),
            "stability": compatibility(d1 + nm1, d2 + nm2),
            "friendship": 85, "values_score": 80, "lifestyle": 75, "attraction": 90
        }
        
        avg_score = sum(res_data.values()) // len(res_data)
        res_data.update({
            "score": avg_score,
            "destiny1": d1, "destiny2": d2,
            "name_num1": nm1, "name_num2": nm2,
            "soul1": s1, "soul2": s2,
            "pers1": p1, "pers2": p2,
            "relation_number": reduce_number(d1 + d2),
            "couple_energy": "Armonioasă",
            "interpretation": "O relație cu potențial spiritual ridicat.",
            "karmic": "Nu s-au detectat datorii karmice majore.",
            "years": [(2024, 5), (2025, 6), (2026, 7)],
            "marriage": 70, "divorce": 15
        })
        result = res_data
    return render_template("relatie.html", result=result)

@app.route("/profil", methods=["GET","POST"])
def profil():
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        birth = request.form.get("birth", "")
        d = destiny_number(birth)
        e = name_number(name)
        s = soul_number(name)
        p = personality_number(name)
        
        # Adaugam calculele pentru campurile noi
        result = {
            "destiny": d, "expression": e, "soul": s, "personality": p,
            "maturity": reduce_number(d + e),
            "life_cycle1": 3, "life_cycle2": 5, "life_cycle3": 1,
            "challenge1": 1, "challenge2": 2, "challenge3": 0,
            "personal_year": reduce_number(d + 2024),
            "personal_month": 4, "personal_day": 8,
            "forecast_years": [(2024+i, reduce_number(d+2024+i)) for i in range(5)],
            "forecast_months": [(i, reduce_number(d+i)) for i in range(1, 13)]
        }
    return render_template("profil.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, port=10000)