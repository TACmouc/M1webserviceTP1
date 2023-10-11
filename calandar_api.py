from flask import Flask, request, jsonify
import calendar
import datetime
import locale
import sqlite3, re

app = Flask(__name__)

# Connexion à la base de données SQLite
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Création de la table tasks si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT
    )
''')
conn.commit()

@app.route('/calendrier', methods=['GET'])
def get_calendar():
    try:
        # Récupérer le mois et l'année à partir des paramètres de requête
        month = int(request.args.get('month'))
        year = int(request.args.get('year'))

        # Vérifier que le mois et l'année sont valides
        if month < 1 or month > 12 or year < 0:
            return jsonify({"error": "Mois ou année non valides"}), 400

        # Définir la localisation française
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        # Générer le calendrier pour le mois donné
        cal = calendar.monthcalendar(year, month)

        # Créer une liste des jours du mois avec les noms des jours en français
        days = []
        for week in cal:
            for day in week:
                if day != 0:
                    # Obtenir le nom du jour de la semaine en français
                    day_name = datetime.date(year, month, day).strftime("%A")
                    days.append({"day": day, "day_name": day_name})

        # Retourner les jours du mois en tant que réponse JSON
        return jsonify({"month": month, "year": year, "days": days})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/calendrier/add_task', methods=['POST'])
def add_task():
    try:
        # Récupérer les données JSON de la requête
        data = request.json

        # Extraire la date et la tâche de la requête
        date = data.get('date')
        task = data.get('task')

        # Vérifier si la date est valide
        if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date):
            # Insérer la tâche dans la base de données
            cursor.execute('INSERT INTO tasks (date, description) VALUES (?, ?)', (date, task))
            conn.commit()

            return jsonify({"message": "Tâche ajoutée avec succès"})
        else:
            return jsonify({"error": "Date non valide"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calendrier/tasks', methods=['GET'])
def get_tasks():
    try:
        # Récupérer la date à partir des paramètres de requête
        date_str = request.args.get('date')

        # Vérifier si la date est valide
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Date non valide"}), 400

        # Récupérer les tâches associées à la date depuis la base de données
        cursor.execute('SELECT description FROM tasks WHERE date = ?', (date,))
        tasks_list = [row[0] for row in cursor.fetchall()]

        return jsonify({"date": date_str, "tasks": tasks_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)