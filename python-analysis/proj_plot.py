import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
PATH = r'C:\Users\SEVENS\data_analysis.csv'
import csv
import pandas as pd
import time
time_orig = 
def live_graph(i):
#time.sleep(2)
  with open (PATH,'r') as fp:
    data = csv.DictReader()
    df = pd.DataFrame(data)
    hum_y_val = df['Humidity']
    tem_y_val = df['Temperature']
    time_curr = time()
    plt.plot(time,hum_y_val)
    plt.legend(loc='upper left')
    plt.xlabel('Time in Secs')
    plt.ylabel('Humidity and Temperature')
    plt.cla()
    plt.show()


ani = Animation(plt.gcf,live_graph,interval=2000)