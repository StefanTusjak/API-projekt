# 🧪 Flask API & Frontend Demo pro výuku testování

Tento projekt slouží jako jednoduchá výuková ukázka propojení **backendu (Flask + MySQL)** s **frontendem (HTML + JavaScript)**. Obsahuje správný i záměrně chybný formulář, podporuje testování pomocí Postmanu i Pytestu, a obsahuje všechny základní operace (CRUD).

---

## 🔧 Co všechno aplikace umí

| Funkce | URL / Akce | Popis |
|--------|------------|--------|
| ✅ Přidání uživatele | `/` | Validovaný formulář |
| ✅ Výpis uživatelů | `/users` + frontend | Načítání seznamu uživatelů přes API |
| ✅ Hledání uživatelů | `/users?search=něco` | Vyhledávání podle jména nebo e-mailu |
| ✅ Úprava uživatele | Frontend + `PUT /users` | In-place editace |
| ✅ Smazání uživatele | Frontend + `DELETE /users` | Přes tlačítko |
| ❌ Chybný formulář | `/form-test` | Formulář s chybami pro testování |
| ✅ Automatizované testy | `test_api.py` | Pomocí `python test_api.py` |

---

## 📦 Požadavky

- Python 3.8+
- MySQL (např. pomocí MySQL Workbench)
- Webový prohlížeč

### 🔌 Python knihovny

- Instalace flasku
```bash
pip install flask
```
- Pokud nemáš tak instalace knihovny pro MySQL
```bash
pip install mysql-connector-python
```

---

## 🛠 Nastavení databáze

1. Vytvoř si databázi ve Workbench `student`:

```sql
CREATE DATABASE student;
```

2. V databázi spusť následující SQL pro vytvoření tabulky:

```sql
CREATE TABLE uzivatele (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jmeno VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);
```

---

## 🚀 Jak to spustit

1. Ujisti se, žev souboru `api.py` máš správně nastaveno připojení k MySQL a ujisti se, že se nacházíš v souboru api.py:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",       # uprav podle svého
    password="",   # uprav podle svého
    database="student"
)
```

2. Spusť Flask server:
- Buď příkazem: 
```bash
python api.py
```
- nebo šipkou vpravo nahoře 

3. Otevři prohlížeč:

```
http://localhost:8000/
```

---

## 🧪 Automatizované testy

Projekt obsahuje soubor `test_api.py`, kde jsou otestovány:

- vytvoření uživatele (včetně chybových stavů),
- validace e-mailu,
- duplicita,
- úprava a smazání.

Spusť testy takto:

```bash
python test_api.py
```

> Nevolá se pomocí `pytest`, protože některé funkce vrací `return`, aby se dalo řídit pořadí testů.

---

## 👨‍🎓 Pro výuku

- `/form-test` slouží k testování špatného návrhu formuláře
- správný formulář je na `/`
- vše je testovatelné i přes Postman (API endpointy jsou RESTové)

---

## 📁 Struktura projektu

```
/projekt/
│
├── api.py                # Flask backend
├── test_api.py           # Automatické testy
├── /templates/
│   ├── index.html        # Správný formulář
│   └── form_test.html    # Chybný formulář
└── README.md             # Tento popis
```

---

## 📬 Kontakt / Autor

Projekt pro výuku v rámci kurzu testování s Pythonem.  
Připravil: **Štefan Tusjak**
