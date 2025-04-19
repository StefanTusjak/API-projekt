from flask import Flask, request, jsonify, render_template
import mysql.connector
import re

app = Flask(__name__)

# Připojení k MySQL databázi
db = mysql.connector.connect(
    host="localhost",
    user="root",         # Změň dle svého nastavení
    password="1111",     # Změň dle svého nastavení
    database="student"   # Změň dle své databáze
)

# Úvodní stránka s formulářem
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form-test")
def form_test():
    return render_template("form_test.html")

# Získání všech uživatelů
@app.route("/users", methods=["GET"])
def get_users():
    search = request.args.get("search", "").strip()
    cursor = db.cursor(dictionary=True)

    if search:
        query = """
            SELECT * FROM uzivatele
            WHERE jmeno LIKE %s OR email LIKE %s
        """
        like_search = f"%{search}%"
        cursor.execute(query, (like_search, like_search))
    else:
        cursor.execute("SELECT * FROM uzivatele")

    users = cursor.fetchall()
    return jsonify(users)

# Získání jednoho uživatele podle ID
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM uzivatele WHERE id = %s", (id,))
    user = cursor.fetchone()
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Uživatel nenalezen"}), 404

# Vytvoření nového uživatele
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    jmeno = data.get("jmeno", "").strip()
    email = data.get("email", "").strip()

    # 1️Kontrola, že pole nejsou prázdná
    if not jmeno or not email:
        return jsonify({"error": "Jméno a e-mail nesmí být prázdné"}), 400

    # 2️Validace formátu e-mailu (základní)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Neplatný formát e-mailu"}), 400

    # 3️Vložení s odchycením duplicitního e-mailu
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO uzivatele (jmeno, email) VALUES (%s, %s)", (jmeno, email))
        db.commit()
        return jsonify({"message": "Uživatel vytvořen", "id": cursor.lastrowid}), 201

    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Uživatel s tímto e-mailem již existuje"}), 409
        else:
            return jsonify({"error": "Chyba při zápisu do databáze"}), 500

# Aktualizace existujícího uživatele
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    jmeno = data.get("jmeno", "").strip()
    email = data.get("email", "").strip()

    if not jmeno or not email:
        return jsonify({"error": "Jméno a e-mail nesmí být prázdné"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Neplatný formát e-mailu"}), 400

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE uzivatele SET jmeno = %s, email = %s WHERE id = %s", (jmeno, email, id))
        db.commit()
        return jsonify({"message": "Uživatel aktualizován"}), 200

    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "E-mail již existuje u jiného uživatele"}), 409
        else:
            return jsonify({"error": "Chyba při aktualizaci"}), 500

# Smazání uživatele
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM uzivatele WHERE id = %s", (id,))
    db.commit()
    return jsonify({"message": "Uživatel smazán"}), 200

# Spuštění aplikace
if __name__ == "__main__":
    app.run(debug=True, port=8000)
