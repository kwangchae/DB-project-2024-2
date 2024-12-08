from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# DB 연결
def get_db_connection():
    conn = sqlite3.connect('F1_2024.db')
    conn.row_factory = sqlite3.Row
    return conn

# 메인 페이지 라우팅
@app.route('/')
def index():
    conn = get_db_connection()
    drivers = conn.execute('SELECT * FROM Driver ORDER BY DriverPts DESC').fetchall()
    teams = conn.execute('SELECT * FROM Team ORDER BY TeamPts DESC').fetchall()
    conn.close()
    return render_template('index.html', drivers=drivers, teams=teams)

# 드라이버 페이지 라우팅
@app.route('/drivers/')
def show_drivers():
    conn = get_db_connection()
    drivers = conn.execute('SELECT * FROM Driver ORDER BY DriverPts DESC').fetchall()
    conn.close()
    return render_template('drivers.html', drivers=drivers)

# 팀 목록 
@app.route('/teams/')
def show_teams():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM Team ORDER BY TeamPts DESC').fetchall()
    conn.close()
    return render_template('teams.html', teams=teams)

# 서킷 목록
@app.route('/circuits/')
def show_circuits():
    conn = get_db_connection()
    circuits = conn.execute('SELECT * FROM Circuit ORDER BY Date').fetchall()
    conn.close()
    return render_template('circuits.html', circuits=circuits)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)