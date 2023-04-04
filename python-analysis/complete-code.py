# libraries

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import re
from itertools import count
import numpy as np
import pandas as pd

# declaration of variables

counting_factor = count()
hum = []
tem = []
fac = []
pattern = re.compile(r'-?\d+\.?\d*')
PATH = r'data_analysis.csv'  # file path to .csv file
fieldnames = ['Humidity', 'Temperature']  # csv header lines


def extract_data() -> list:
    """
    reads from a csv file to obtain temperature and humidity
    values.
    :return: 2 lists containing temperature and humidity values.
    """
    df = pd.read_csv(PATH)
    df.dropna()
    df.columns = ['Humidity', 'Temperature']
    return [df['Humidity'].tolist(), df['Temperature'].tolist()]


def generate_time():
    """
  generates a list of time values using a generator
  created by count.
  #TO DO: Use time.time()
  :return: list of time values.
  """
    current_time = next(counting_factor)
    fac.append(current_time)
    return fac


# plots a live graph from the extracted data

def plot_live_graph():
    """
    reads data from arduino via serial communication and writes to a csvfile to store the data,
    also stores the plotting values for humidity and temperature as floats, for every call
    the length of values stored increases as it appends to the same line for every line
    read. This means that a new graph is generated every time the function is called therefore can
    be passed as an argument to funcAnimation to generate a live graph.
  :return: None
  """
    try:
        ser = serial.Serial('COM5', 9600)  # Replace 'COM#' with the appropriate port number
        if len(fac) == 0:
            print('reading data ...')
        line = ser.readline().decode('utf-8').strip()
        s = [float(s) for s in pattern.findall(line)]
        hum.append(s[0])
        tem.append(s[1])
        print(line)
        df = pd.DataFrame({'Humidity': hum, 'Temperature': tem})
        df.to_csv(PATH, index=False)

        variables = extract_data()
        my_time = generate_time()
        humty = variables[0]
        tempr = variables[1]

        plt.cla()
        plt.plot(my_time, humty, color='red', linewidth=1, linestyle='--', label='Humidity')
        plt.plot(my_time, tempr, color='green', linewidth=1, linestyle='--', label='Temperature')
        plt.xlabel('Time (s)')
        plt.ylabel('Humidity(%) and Temperature (C)')
        plt.legend(loc='upper right')
        if len(humty) % 240 == 0:
            humidity_for_pie = np.average(humty)
            temperature_for_pie = np.average(tempr)
            plt.pie([humidity_for_pie, temperature_for_pie], labels=['Humidity (%)', 'Temperature (C)'])
            plt.savefig(r'proj_pic_pie.png')
        if len(humty) % 288 == 0:
            plt.scatter(my_time, humty, color='red')
            plt.scatter(my_time, tempr, color='green')
            plt.savefig(r'proj_pic_scatter.png')
    except serial.SerialException:
        print('failed to read port ...')

# repeatedly calls plot_live_graph after 2.5 seconds to create a live graph


ani = FuncAnimation(plt.gcf(), plot_live_graph, frames=100, interval=2500)
plt.show()
plt.tight_layout()
plt.style.use('fivethirtyeight')
