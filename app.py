from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)

# פונקציה לחישוב ספירת העומר
def get_omer_count():
    start_date = datetime.date(2025, 4, 5)  # תאריך התחלה (היום הראשון של פסח)
    today = datetime.date.today()
    delta = today - start_date
    return delta.days + 1

@app.route('/api/times')
def get_times():
    url = 'https://calendar.2net.co.il/todaytimes.aspx?city=%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9F'
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'בעיה בקבלת נתונים מהאתר'}), 500

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'TodayZmanim'})
        if not table:
            return jsonify({'error': 'לא נמצאה טבלה עם id=TodayZmanim'}), 500

        times = []
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                label = cells[0].text.strip()
                time = cells[1].text.strip()
                times.append({'label': label, 'time': time})

        # הוספת זמני ספירת העומר והודעת הגבאים
        omr_day = get_omer_count()
        gabbai_message = "אנא עקוב אחרי ההוראות החדשות להמשך היום."

        return render_template('index.html', times=times, omr_day=omr_day, gabbai_message=gabbai_message)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'בעיה בטעינת הנתונים'}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
