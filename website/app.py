from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 

API_KEY = "api_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None

    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial'
            response = requests.get(url)
            if response.status_code == 200:
                weather = response.json()
                if city not in session['history']:
                    session['history'].append(city)
                    session.modified = True
            else:
                error = "City not found. Please try again."
    elif request.method == 'GET' and 'city' in request.args:
        city = request.args.get('city')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial'
        response = requests.get(url)
        if response.status_code == 200:
            weather = response.json()
        else:
            error = "City not found. Please try again."

    return render_template('index.html', weather=weather, error=error, history=session['history'])

if __name__ == '__main__':
    app.run(debug=True)
