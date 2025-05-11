import mysql.connector

# Set your DB config here
db_config = {
    'host': 'localhost',
    'user': 'tomadmin',
    'password': 'BlackSage44$',
    'database': 'golfdb'
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Drop tables if they exist
cursor.execute("DROP TABLE IF EXISTS slots")
cursor.execute("DROP TABLE IF EXISTS courses")

# Create courses table
cursor.execute("""
    CREATE TABLE courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
""")

# Create slots table
cursor.execute("""
    CREATE TABLE slots (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_id INT,
        date DATE,
        time TIME,
        price DECIMAL(10,2),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
""")

print("Tables `courses` and `slots` created successfully.")

# Close connection
cursor.close()
conn.close()
