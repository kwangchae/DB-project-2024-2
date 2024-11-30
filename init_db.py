import pandas as pd
import sqlite3

# 엑셀 파일 로든
file_path = 'F1_DB8.xlsx' # 코드와 동일경로
excel_data = pd.ExcelFile(file_path)

conn = sqlite3.connect('F1_2024.db')
cursor = conn.cursor()

# 드라이버 테이블
cursor.execute('''
CREATE TABLE IF NOT EXISTS Driver (
    DriverNo INTEGER PRIMARY KEY,
    DriverName TEXT,
    DriverPts INTEGER,
    DriverComment TEXT,
    TeamID TEXT,
    FOREIGN KEY (TeamID) REFERENCES Team (TeamName)
)
''')
# 팀 테이블
cursor.execute('''
CREATE TABLE IF NOT EXISTS Team (
    TeamName TEXT PRIMARY KEY,
    TeamPts INTEGER,
    TeamComment TEXT
)
''')

driver_pts = {}
team_pts = {}

for sheet_name in excel_data.sheet_names[1:]:
    sheet_data = excel_data.parse(sheet_name)
    for _, row in sheet_data.iterrows():
        try:
            driver_no = int(row['Unnamed: 2'])
            driver_name = row['Unnamed: 3']
            team_name = row['Unnamed: 10']
            pts = int(row['Unnamed: 6']) if pd.notna(row['Unnamed: 6']) else 0
            
            # 드라이버 pts 취합
            driver_pts[driver_no] = driver_pts.get(driver_no, {'name': driver_name, 'pts': 0, 'team': team_name})
            driver_pts[driver_no]['pts'] += pts

            # 팀 pts 취합
            team_pts[team_name] = team_pts.get(team_name, 0) + pts

        except Exception as e:
            continue

# 드라이버 pts, 팀 정보(외래키) 추가
for driver_no, info in driver_pts.items():
    cursor.execute('''
        INSERT INTO Driver (DriverNo, DriverName, DriverPts, DriverComment, TeamID)
        VALUES (?, ?, ?, ?, ?)
    ''', (driver_no, info['name'], info['pts'], None, info['team']))
# 팀 이름, 팀 pts 추가
for team_name, total_pts in team_pts.items():
    cursor.execute('''
        INSERT INTO Team (TeamName, TeamPts, TeamComment)
        VALUES (?, ?, ?)
    ''', (team_name, total_pts, None))

conn.commit()
conn.close()

print("DB completed.")