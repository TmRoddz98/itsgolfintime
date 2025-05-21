from flask import Flask, render_template, request
import mysql.connector
import datetime
from zoneinfo import ZoneInfo
from astral import LocationInfo
from astral.sun import sun

app = Flask(__name__)

# DB connection settings
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="",
        password="",
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
    curdate = datetime.date.today()
    curtime = datetime.datetime.now(ZoneInfo("Europe/London")).time()
    curtime = str(curtime)[:5]
    london = LocationInfo("London", "England", "Europe/London", 51.5074, -0.1278)
    s = sun(london.observer, date=curdate, tzinfo=london.timezone)
    endtime = str(s['sunset'].time())[:5]
    print(endtime)
    return render_template('index.html', courses=courses,curdate=curdate,curtime=curtime, endtime=endtime)

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
  