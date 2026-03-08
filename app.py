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
        # Preluare date jucători
        p1_name = request.form.get("player1", "")
        p2_name = request.form.get("player2", "")
        b1 = request.form.get("birth1", "")
        b2 = request.form.get("birth2", "")
        
        # Preluare date meci (pentru Energia Meciului)
        match_date = request.form.get("date", "")
        match_time = request.form.get("time", "") # ex: "14:30"
        location = request.form.get("tournament", "")
        surface = request.form.get("surface", "")
        round_name = request.form.get("round", "")

        # 1. Calcule Vibratii Energie Meci
        day_vib = destiny_number(match_date) if match_date else 0
        
        # Vibratia orei (adunăm cifrele orei și minutelor)
        hour_digits = re.sub(r"\D", "", match_time)
        hour_vib = reduce_number(sum(int(d) for d in hour_digits)) if hour_digits else 0
        
        loc_vib = name_number(location) if location else 0
        surf_vib = name_number(surface) if surface else 0
        round_vib = name_number(round_name) if round_name else 0
        
        # Energia completa (suma tuturor vibrațiilor meciului)
        event_energy = reduce_number(day_vib + hour_vib + loc_vib + surf_vib + round_vib)

        # 2. Calcule Jucători
        d1, d2 = destiny_number(b1), destiny_number(b2)
        n1, n2 = name_number(p1_name), name_number(p2_name)
        
        # Energia personală a zilei (Destin + Vibrația zilei)
        p1_personal_day = reduce_number(d1 + day_vib)
        p2_personal_day = reduce_number(d2 + day_vib)
        
        # Scoruri bazate pe compatibilitatea cu energia evenimentului
        s1_score = compatibility(p1_personal_day, event_energy)
        s2_score = compatibility(p2_personal_day, event_energy)
        
        # 3. Probabilități
        total = s1_score + s2_score
        prob1 = round((s1_score / total) * 100) if total > 0 else 50
        prob2 = 100 - prob1

        result = {
            "player1": p1_name, 
            "player2": p2_name,
            "day": day_vib, 
            "hour": hour_vib, 
            "location": loc_vib, 
            "surface": surf_vib, 
            "round": round_vib, 
            "event": event_energy, 
            "pressure": compatibility(event_energy, 9), # Presiunea vs cifra de putere 9
            "p1": {
                "destiny": d1, 
                "name": n1, 
                "year": reduce_number(d1 + datetime.datetime.now().year), 
                "personal": p1_personal_day, 
                "score": s1_score
            },
            "p2": {
                "destiny": d2, 
                "name": n2, 
                "year": reduce_number(d2 + datetime.datetime.now().year), 
                "personal": p2_personal_day, 
                "score": s2_score
            },
            "prob1": prob1, 
            "prob2": prob2,
            "prediction": p1_name if prob1 > prob2 else p2_name
        }
        
        # Calcul probabilitate Bookmaker (dacă există cote)
        o1 = request.form.get("odds1")
        o2 = request.form.get("odds2")
        if o1 and o2:
            try:
                b_p1 = (1/float(o1)) / ((1/float(o1)) + (1/float(o2))) * 100
                result["book_prob1"] = round(b_p1, 1)
                result["book_prob2"] = round(100 - b_p1, 1)
                result["value1"] = round(prob1 - b_p1, 1)
                result["value2"] = round(prob2 - (100 - b_p1), 1)
            except: pass

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

# if __name__ == "__main__":
#     # Render furnizează portul prin variabila de mediu PORT
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)