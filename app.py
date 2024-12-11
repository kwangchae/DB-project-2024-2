from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB 연결
def get_db_connection():
    conn = sqlite3.connect('F1_2024.db')
    conn.row_factory = sqlite3.Row
    return conn

# 메인 페이지
@app.route('/')
def index():
    conn = get_db_connection()
    drivers = conn.execute('SELECT * FROM Driver ORDER BY DriverPts DESC').fetchall()
    teams = conn.execute('SELECT * FROM Team ORDER BY TeamPts DESC').fetchall()
    conn.close()
    return render_template('index.html', drivers=drivers, teams=teams)

##################
# 드라이버 페이지 # 
##################
@app.route('/drivers/')
def show_drivers():
    conn = get_db_connection()
    drivers = conn.execute('SELECT * FROM Driver ORDER BY DriverPts DESC').fetchall()
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        drivers = conn.execute('''
            SELECT * FROM Driver WHERE DriverName LIKE ? ORDER BY DriverPts DESC
        ''', (f'{search_query}%',)).fetchall()
    else:
        drivers = conn.execute('SELECT * FROM Driver ORDER BY DriverPts DESC').fetchall()
    conn.close()
    return render_template('drivers.html', drivers=drivers)

# 드라이버 정보
@app.route('/driver/<int:driver_no>')
def driver_details(driver_no):
    conn = get_db_connection()
    driver = conn.execute('SELECT * FROM Driver WHERE DriverNo = ?', (driver_no,)).fetchone()
    results = conn.execute('''
        SELECT r.*, c.CircuitName
        FROM Results r, Circuit c
        WHERE r.CircuitID = c.CircuitID
            AND r.DriverNo = ?
        ORDER BY c.Date;
    ''', (driver_no,)).fetchall()
    conn.close()
    return render_template('driver_details.html', driver=driver, results=results)

# 코멘트 추가/수정
@app.route('/edit_comment/<int:driver_no>', methods=['POST'])
def edit_comment(driver_no):
    new_comment = request.form['new_comment']
    conn = get_db_connection()
    conn.execute('UPDATE Driver SET DriverComment = ? WHERE DriverNo = ?', (new_comment, driver_no))
    conn.commit()
    conn.close()
    return redirect(url_for('show_drivers'))

# 코멘트 초기화 (''로 업데이트)
@app.route('/delete_comment/<int:driver_no>', methods=['POST'])
def delete_comment(driver_no):
    conn = get_db_connection()
    conn.execute('UPDATE Driver SET DriverComment = ? WHERE DriverNo = ?', ('', driver_no))
    conn.commit()
    conn.close()
    return redirect(url_for('show_drivers'))


############
# 팀 페이지 # 
############
@app.route('/teams/')
def show_teams():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM Team ORDER BY TeamPts DESC').fetchall()
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        teams = conn.execute('''
            SELECT * FROM Team WHERE TeamName LIKE ? ORDER BY TeamPts DESC
        ''', (f'{search_query}%',)).fetchall()
    else:
        teams = conn.execute('SELECT * FROM Team ORDER BY TeamPts DESC').fetchall()
    conn.close()
    return render_template('teams.html', teams=teams)

# 팀 정보 
@app.route('/team/<string:team_name>')
def team_details(team_name):
    conn = get_db_connection()
    team = conn.execute('SELECT * FROM Team WHERE TeamName = ?', (team_name,)).fetchone()
    drivers = conn.execute('SELECT * FROM Driver WHERE TeamID = ?', (team_name,)).fetchall()
    results = conn.execute('''
        SELECT r.*, c.CircuitName, d.DriverName
        FROM Results r, Circuit c, Driver d
        WHERE r.CircuitID = c.CircuitID
            AND r.DriverNo = d.DriverNo
            AND r.TeamName = ?
        ORDER BY c.Date;
    ''', (team_name,)).fetchall()
    conn.close()
    return render_template('team_details.html', team=team, drivers=drivers, results=results)

# 코멘트 추가/수정
@app.route('/edit_team_comment/<string:team_name>', methods=['POST'])
def edit_team_comment(team_name):
    new_comment = request.form.get('new_comment')
    conn = get_db_connection()
    conn.execute('UPDATE Team SET TeamComment = ? WHERE TeamName = ?', (new_comment, team_name))
    conn.commit()
    conn.close()
    return redirect(url_for('show_teams'))
# 코멘트 초기화
@app.route('/delete_team_comment/<string:team_name>', methods=['POST'])
def delete_team_comment(team_name):
    conn = get_db_connection()
    conn.execute('UPDATE Team SET TeamComment = ? WHERE TeamName = ?', ('', team_name))
    conn.commit()
    conn.close()
    return redirect(url_for('show_teams'))

##############
# 서킷 페이지 #
##############
@app.route('/circuits/')
def show_circuits():
    conn = get_db_connection()
    circuits = conn.execute('SELECT * FROM Circuit ORDER BY Date').fetchall()
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        circuits = conn.execute('''
            SELECT * FROM Circuit WHERE CircuitName LIKE ? ORDER BY Date
        ''', (f'{search_query}%',)).fetchall() 
    else:
        circuits = conn.execute('SELECT * FROM Circuit ORDER BY Date').fetchall()
        
    conn.close()
    return render_template('circuits.html', circuits=circuits)

# 코멘트 추가/수정
@app.route('/edit_circuit_comment/<string:circuit_name>', methods=['POST'])
def edit_circuit_comment(circuit_name):
    new_comment = request.form.get('new_comment')
    conn = get_db_connection()
    conn.execute('UPDATE Circuit SET CircuitComment = ? WHERE CircuitName = ?', (new_comment, circuit_name))
    conn.commit()
    conn.close()
    return redirect(url_for('show_circuits'))

# 코멘트 초기화
@app.route('/delete_circuit_comment/<string:circuit_name>', methods=['POST'])
def delete_circuit_comment(circuit_name):
    conn = get_db_connection()
    conn.execute('UPDATE Circuit SET CircuitComment = ? WHERE CircuitName = ?', ('', circuit_name))
    conn.commit()
    conn.close()
    return redirect(url_for('show_circuits'))

##################
# 경기기록 페이지 # 
##################
@app.route('/results/<int:circuit_id>')
def show_results(circuit_id):
    conn = get_db_connection()
    results = conn.execute('''
        SELECT r.*, c.CircuitName, d.DriverName, r.RaceComment
        FROM Results r, Circuit c, Driver d
        WHERE r.CircuitID = c.CircuitID
            AND r.DriverNo = d.DriverNo
            AND r.CircuitID = ?
        ORDER BY r.Position
    ''', (circuit_id,)).fetchall()
    conn.close()
    return render_template('results.html', results=results)

# 경기 기록 추가
@app.route('/result_add/', methods=['GET', 'POST'])
def add_result():
    conn = get_db_connection()

    # 드라이버와 서킷 데이터를 미리 가져옵니다.
    drivers = conn.execute('SELECT * FROM Driver').fetchall()
    circuits = conn.execute('SELECT * FROM Circuit').fetchall()
    
    if request.method == 'POST':
        driver_no = request.form['driver_no']
        circuit_id = request.form['circuit_id']

        # DB에서 드라이버 기록 존재 여부 확인
        existing_record = conn.execute('SELECT * FROM Results WHERE DriverNo = ? AND CircuitID = ?', (driver_no, circuit_id)).fetchone()

        if existing_record:
            # 이미 기록이 존재하는 경우 경고 전달
            conn.close()
            return render_template('result_add.html', drivers=drivers, circuits=circuits, warning=True)

        # 새로운 기록 추가
        position = int(request.form['position'])
        pts = int(request.form['pts'])
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        seconds = float(request.form['seconds'])
        race_time = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
        team_name = conn.execute('SELECT TeamID FROM Driver WHERE DriverNo = ?', (driver_no,)).fetchone()[0]
        
        conn.execute('''
            INSERT INTO Results (DriverNo, CircuitID, Position, Pts, Time, TeamName)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (driver_no, circuit_id, position, pts, race_time, team_name))
        conn.commit()
        conn.close()
        return redirect(url_for('show_results', circuit_id=circuit_id))

    # GET 요청일 경우
    conn.close()
    return render_template('result_add.html', drivers=drivers, circuits=circuits, warning=False)

# 경기 기록 삭제
@app.route('/delete_result/<int:result_id>', methods=['POST'])
def delete_result(result_id):
    conn = get_db_connection()

    # CircuitID를 가져와 삭제 후 해당 서킷 결과 페이지로 리다이렉트
    circuit_id = conn.execute('SELECT CircuitID FROM Results WHERE ResultsID = ?', (result_id,)).fetchone()['CircuitID']
    conn.execute('DELETE FROM Results WHERE ResultsID = ?', (result_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_results', circuit_id=circuit_id))

# 코멘트 추가/수정
@app.route('/edit_results_comment/<int:result_ID>', methods=['POST'])
def edit_result_comment(result_ID):
    new_comment = request.form.get('new_comment')
    conn = get_db_connection()
    conn.execute('UPDATE Results SET RaceComment = ? WHERE ResultsID = ?', (new_comment, result_ID))
    
    # result_ID를 포함하는 circuit_id탐색
    circuit_id = conn.execute('SELECT CircuitID FROM Results WHERE ResultsID = ?', (result_ID,)).fetchone()[0]
    conn.commit()
    conn.close()    
    # 해당 circuit_id로 새로고침
    return redirect(url_for('show_results', circuit_id=circuit_id))

# 코멘트 초기화
@app.route('/delete_results_comment/<int:result_ID>', methods=['POST'])
def delete_result_comment(result_ID):
    conn = get_db_connection()
    conn.execute('UPDATE Results SET RaceComment = ? WHERE ResultsID = ?', ('', result_ID))
    circuit_id = conn.execute('SELECT CircuitID FROM Results WHERE ResultsID = ?', (result_ID,)).fetchone()[0]
    conn.commit()
    conn.close()
    return redirect(url_for('show_results', circuit_id=circuit_id))

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)