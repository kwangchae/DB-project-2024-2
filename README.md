# F1 Racing Dashboard

F1 Racing Dashboard는 Flask를 사용하여 개발된 웹 애플리케이션으로, F1 드라이버, 팀, 서킷, 레이스 결과를 관리하고 조회할 수 있습니다. 사용자는 드라이버와 팀의 상세 정보, 레이스 결과를 조회하거나 검색 기능을 통해 원하는 데이터를 쉽게 찾을 수 있습니다.

## 기능

1. **홈페이지**
   - 드라이버와 팀의 포인트 순위 표기
   - 검색 기능 제공

2. **드라이버 관리**
   - 드라이버 목록 조회
   - 드라이버 상세 정보 및 레이스 결과 조회
   - 드라이버 코멘트 추가 및 수정

3. **팀 관리**
   - 팀 목록 조회
   - 팀 상세 정보 및 소속 드라이버, 레이스 결과 조회

4. **서킷 관리**
   - 서킷 목록 조회
   - 특정 서킷의 레이스 결과 확인

5. **레이스 결과 관리**
   - 각 레이스 결과 확인
   - 코멘트 추가 및 삭제

## 설치 방법

1. **Python 환경 설정**
   - Python 3.7 이상 설치

2. **의존성 패키지 설치**
   ```bash
   pip install -r requirements.txt

.
├── app.py                  # Flask 애플리케이션 메인 파일
├── templates/              # HTML 템플릿 디렉토리
│   ├── index.html
│   ├── drivers.html
│   ├── teams.html
│   ├── circuits.html
│   ├── driver_details.html
│   ├── team_details.html
│   ├── results.html
│   └── edit_comment.html
├── static/                 # 정적 파일 (CSS, JS, 이미지)
│   └── style.css
├── F1_Racing.db            # SQLite 데이터베이스 파일
├── requirements.txt        # 의존성 패키지 목록
└── README.md               # 프로젝트 설명 파일
