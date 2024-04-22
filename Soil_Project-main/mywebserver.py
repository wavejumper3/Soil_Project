from flask import Flask, render_template
app = Flask(__name__)
import sqlite3

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('/home/pi/Desktop/Soil_Project-main/community_garden.db')
    c = conn.cursor()
    # Query data from the database
    c.execute('SELECT date, temp, humid, soil, light_duration FROM garden_data;')
    data = c.fetchall()
    # Close the database connection
    conn.close()
    # Pass data to the template and render the webpage
    return render_template('data.html', data=data)

if __name__ == "__main__": 
	app.run(host="0.0.0.0", port=80, debug=True)
