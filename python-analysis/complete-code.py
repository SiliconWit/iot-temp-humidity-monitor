#libraries

import csv 
import pandas as pd
import PIL
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import re
from itertools import count
import os
import numpy as np
#declaration of variables

counting_factor = count()
hum = []
tem = []
fac = []
pattern = re.compile(r'-?\d+\.?\d*')
PATH = r'C:\Users\SEVENS\group_work_8\data_analysis.csv' #file path to .csv file 
fieldnames = ['Humidity','Temperature'] #csv header lines
#if os.path.exists(PATH):
  #os.remove(PATH)
#extract data from csv file
def extract_data():
  hum_empty_list = []
  tem_empty_list = []
  with open(PATH,'r') as rf:
    data = csv.reader(rf)
    #hum_vals = data['Humidity'].values.tolist()
    #tem_vals = data['Temperature'].values.tolist()
    #Df_hum = pd.DataFrame(int(hum_vals))
    #Df_hum = pd.DataFrame(int(tem_vals))
    #print(type(Df_hum.values.tolist()))
    big_list = list(data)
    for h_t_list in big_list:
      if len(h_t_list) == 0 or h_t_list == ['Humidity', 'Temperature']:
        pass
      else:
        hum_variabs,tem_variabs = float(h_t_list[0]),float(h_t_list[1])
        hum_empty_list.append(hum_variabs)
        tem_empty_list.append(tem_variabs)
  return [hum_empty_list,tem_empty_list]

# time variable
def generate_time():
  current_time = next(counting_factor)
  fac.append(current_time)
  return fac
#plots a live graph from the extracted data

def plot_live_graph(i):
  try:
    ser = serial.Serial('COM7', 9600)  # Replace 'COM#' with the appropriate port number
    if len(fac) == 0:
      print('reading data ...')
    line = ser.readline().decode('utf-8').strip()
    s = [float(s) for s in pattern.findall(line)]
    hum.append(s[0])
    tem.append(s[1])
    print(line)
    with open (PATH,'w') as fp:
      writer = csv.DictWriter(fp,fieldnames=fieldnames)
      writer.writeheader()
      for index,value in enumerate(range(len(hum))):
        writer.writerow({'Humidity':hum[index],'Temperature':tem[index]})
  
  
    variables = extract_data()
    my_time = generate_time()
    humty = variables[0]
    tempr = variables[1]

    plt.cla()
    plt.plot(my_time,humty,color='red',linewidth=1,linestyle='--',label='Humidity')
    plt.plot(my_time,tempr,color='green',linewidth=1,linestyle='--',label='Temperature')
    plt.xlabel('Time (s)')
    plt.ylabel('Humidity(%) and Temperature (C)')
    plt.legend(loc='upper right')
    if len(humty)%240 == 0:
      humidity_for_pie = np.average(humty)
      temperature_for_pie = np.average(tempr)
      plt.pie([humidity_for_pie,temperature_for_pie],labels=['Humidity (%)','Temperature (C)'])
      plt.savefig(r'C:\Users\SEVENS\group_work_8\proj_pic_pie.png')
    if len(humty)%288 == 0:
       plt.scatter(my_time,humty,color='red')
       plt.scatter(my_time,tempr,color='green')
       plt.savefig(r'C:\Users\SEVENS\group_work_8\proj_pic_scatter.png')
  except serial.SerialException:
    print('failed to read port ...')
  #else:
    #print('something went wrong :( ')

#get current figures then plot the updated graph

ani = FuncAnimation(plt.gcf(),plot_live_graph,interval=2500)
plt.show()
plt.tight_layout()
plt.style.use('fivethirtyeight')


    
    