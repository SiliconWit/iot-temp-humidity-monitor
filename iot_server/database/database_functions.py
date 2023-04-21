import sqlite3
import re
from flask import Flask, request, render_template, jsonify, send_file
from datetime import date


def create_table():
    """
    dynamically creates a table with its name being today's date.
    """
    table_name = 'data_' + date.today().strftime('%Y_%m_%d')
    columns = ["temperature", "humidity", "time"]
    conn = sqlite3.connect('C:/Users/shapz/Desktop/iot-server/database/iot_data.db')
    c = conn.cursor()
    column_str = ', '.join([f"{column} real" for column in columns])
    c.execute(f"CREATE TABLE {table_name} ({column_str})")
    conn.commit()
    conn.close()
    
    
def check_table():
    """
    Checks if a table for today's date exists.
    """
    table_name = 'data_' + date.today().strftime('%Y_%m_%d')
    conn = sqlite3.connect('C:/Users/shapz/Desktop/iot-server/database/iot_data.db')
    c = conn.cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    c.execute(query, (table_name,))
    status = c.fetchone() is not None
    conn.close()
    return status


def updater(temp, hum, time):
    """
    inserts new table values. 
    """
    conn = sqlite3.connect('C:/Users/shapz/Desktop/iot-server/database/iot_data.db')
    c = conn.cursor()
    if check_table():
        table_name = 'data_' + date.today().strftime('%Y_%m_%d')
    else:
        create_table()
        table_name = 'data_' + date.today().strftime('%Y_%m_%d')
        
    values = [(temp, hum, time)]
    c.executemany(f"INSERT INTO {table_name} VALUES (?, ?, ?)", values)
    conn.commit()
    conn.close()
    
    
def display_table(table_name='data_' + date.today().strftime('%Y_%m_%d')):
    """
    handles the display of a table for a given webpage.
    """
    conn = sqlite3.connect('C:/Users/shapz/Desktop/iot-server/database/iot_data.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM {table_name}')
    data = c.fetchall()
    conn.close()
    return render_template('display_table.html', data=data, message='Data updated successfully!')


def get_dates():
    """
    Gets a list of dates for which data is available
    and returns a list of dates in the format yy-mm-dd.
    """
    conn = sqlite3.connect('C:/Users/shapz/Desktop/iot-server/database/iot_data.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    pattern = r'\d{2}_\d{2}_\d{2}'
    results = c.fetchall()
    dates =[re.findall(pattern, i[0]) for i in results]
    formatted_dates = [re.sub( '_', '-', ''.join(i)) for i in dates]
    conn.close()
    return formatted_dates


def get_table_name(date):
    """
    returns the name of the table selected by the user.
    Assumes that all tables are created in the current century.
    """
    
    table_name = 'data_20' + re.sub('-', '_', date)
    return table_name


def send_image():
    return send_file('templates/image.jpg', mimetype='image/jpeg')
        