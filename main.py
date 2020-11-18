# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import requests
import statistics
from flask import Flask, Markup, redirect, render_template, url_for, request

app = Flask(__name__)

APPID = "019a570554ed0d5c7e359efc0d3ea888"
RESULT_URL = "https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&exclude=alerts,minutely,hourly&units=metric&appid={2}"

labels = [
    'MIN', 'MAX', 'MEAN', 'MEDIAN'
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"
]


@app.route('/weather', methods=['GET', 'POST'])
def weather_forecast():
    """"
    Latitude, longitude geographical coordinates and period to be entered by the user - required
    - textboxes for inputting location coordinates
    - getData click button to request weather results.
    - calculate min, max, mean and average temps\
    ==> tempValues, temp = {min: x, max: yy, average zz
    - return render_template('main.html')
    Example coordinates:
    -  # lat = -25.930149
    # lon = 28.011511
    """
    if request.method == 'POST':
        # API request
        try:
            data = requests.get(RESULT_URL.format(request.form["lat"], request.form["long"], APPID))
        except:
            raise Exception('Location not found!!!')

        daily_data = data.json()["daily"]

        # create dict (min, max and humidity)
        weather = []
        for row in daily_data:
            weather.append({
                'datetimestamp': row['dt'], 'minimum': row['temp']['min'],
                'maximum': row['temp']['max'], 'humidity': row['humidity']
            })

        return render_template('results.html', title='Temperature Bar Chart', cum=weather, data=daily_data)
    else:
        return render_template('main.html')


@app.route('/barchart', methods=['GET'])
def barchart():
    bar_labels=labels

    # Not full implemented - for illustrating charting.
    url_api = "https://api.openweathermap.org/data/2.5/onecall?lat=-25.930149&lon=28.011511&exclude=alerts,minutely,hourly&units=metric&appid={0}".format(
        APPID)
    data = requests.get(url_api)
    daily_data = data.json()["daily"]

    # create dict with min, max and humidity
    weather = []
    min_temps = []
    for row in daily_data:
        weather.append({
            'datetimestamp': row['dt'], 'minimum': row['temp']['min'],
            'maximum': row['temp']['max'], 'humidity': row['humidity']
        })

        # Get list of minimum temperatures
        min_temps.append(row['temp']['min'])

    humidity = daily_data[0]['humidity']
    mean = statistics.mean(min_temps)
    median = statistics.median(min_temps)
    bar_values = [weather[0]['minimum'], weather[0]['maximum'], mean, median]

    return render_template('bar_chart.html', title='Temperature Bar Chart', humidity=humidity, max=60, labels=bar_labels, values=bar_values)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetb  rains.com/help/pycharm/
