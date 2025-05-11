from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# DB connection settings
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="golfdb"
    )

@app.route('/')
def index():
    # Connect to your database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get a list of all available course names
    cursor.execute("SELECT DISTINCT name FROM courses")
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template('index.html', courses=courses)

@app.route('/results', methods=['GET', 'POST'])
def results():
    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT courses.name, slots.date, slots.time, slots.price
        FROM slots
        JOIN courses ON slots.course_id = courses.id
        WHERE date = %s AND time BETWEEN %s AND %s
        ORDER BY price
    """
    cursor.execute(query, (date, start_time, end_time))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('slots.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)