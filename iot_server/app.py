from database import database_functions as d_f
from flask import Flask, request, jsonify, render_template, send_file
from datetime import date
from urllib.parse import unquote_plus

app = Flask(__name__)

# we start by defining routes to resources needed by html files.
@app.route('/about.jpg')
def display_about():
    d_f.send_image()
    return send_file('templates/about.jpg',  mimetype='image/jpeg')

@app.route('/image.jpg')
def display_image():
    d_f.send_image()
    return send_file('templates/image.jpg',  mimetype='image/jpeg')

@app.route('/sky.gif')
def display_sky():
    return send_file('templates/sky.gif',  mimetype='image/gif')

@app.route('/about.pdf')
def get_about():
    return send_file('templates/about.pdf',  mimetype='application/pdf')


# We then define routes for urls.
@app.route('/')
def index():
    return render_template('about.html')
    
@app.route('/dates')
def dropdown():
    data = d_f.get_dates()
    return render_template('dropdown.html', dates=data, message='success')
@app.route('/update', methods=['POST', 'GET'])
def update_data():
    # a get request will be sent by the browser to request a web page.
    if request.method == 'GET':
        # only create a table for the current day if one does not exist.
        date = ''
        try:
            # this try block check the get request to
            # determine if it is from the dropdown list
            # or the client browser.
            date = request.args.get('date')
            name = d_f.get_table_name(date)
            return d_f.display_table(table_name=name)
        except Exception:
            pass
        
        if not d_f.check_table():
            d_f.create_table()
        table = d_f.display_table()
        return table
    else:
        # data is submitted as post request
        # tries to process various types of content types.
        temp, hum, time = [None, None, None]
        try:
            temp = request.form['temperature']
            hum = request.form['humidity']
            time = request.form['time']
        except Exception:
            if request.content_type == 'application/x-www-form-urlencoded':
                temp = unquote_plus(request.form['temperature'])
                hum = unquote_plus(request.form['humidity'])
                time = unquote_plus(request.form['time'])
        
            elif request.content_type == 'application/json':
                data = request.get_json()
                temp = data.get('temperature')
                hum = data.get('humidity')
                time = data.get('time')
            else:
                return jsonify({'message:' "request body could not be parsed, check to ensure that content type is json or form data"})
        if temp is None or hum is None or time is None:
            return jsonify({'message': 'no values given'})
        
        d_f.updater(temp, hum, time)
    
    return jsonify({'message': 'Data updated successfully!'})


if __name__ == '__main__':
    app.run(debug=True)