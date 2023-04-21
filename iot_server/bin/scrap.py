summary =  """
            This module is the development space
            for project_functions and app modules.
            
            Functions are written and tested here before
            being added to their respective modules.
            
            The commented out code represents the various 
            tests that were carried out while developing.
            """


import re
import sqlite3
import requests


from flask import Flask, render_template
from datetime import date
from database import database_functions as d_f

# today_date = date.today()
# print(today_date.strftime("%Y-%m-%d"))


# columns = ["temperature", "humidity", "time"]
# column_str = ', '.join([f"{column} real" for column in columns])
# print(column_str)

# # data_app.create_table()

# if data_app.check_table():
#     print('table exists')


# url = 'http://127.0.0.1:5000/update'
# data = {'temperature': '25', 'humidity': '50', 'time': '2023-04-13 12:00:00'}
# response = requests.post(url, data=data)

# print(response.json())

# conn = sqlite3.connect('C:/Users/shapz/Desktop/iot-server/database/iot_data.db')
# c = conn.cursor()

# # table_name = 'consolidated_data'
# # columns = ["temperature", "humidity", "time", "date"]
# # column_str = ','.join([f'{column} real' for column in columns])
# # c.execute(f'CREATE TABLE {table_name}(column_str)')

# import re
# c.execute("SELECT name FROM sqlite_master WHERE type='table'")
# pattern = r'\d{2}_\d{2}_\d{2}'
# results = c.fetchall()
# dates =[re.findall(pattern, i[0]) for i in results]
# formatted_dates = [re.sub( '_', '-', ''.join(i)) for i in dates]
# print(formatted_dates)

# app = Flask(__name__)



# if __name__ == '__main__':
#     app.run(debug=True)
# print(d_f.get_dates())
