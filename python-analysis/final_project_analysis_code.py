'''
Program  for visual analysis, data from arduino port,relay .png attachments as email.

Port on use is the 'COM12' on arduino. Program reads COM12 using 'Pyserial' module, creates a csv. Program reads from csv and plots a live graph, pie chart and scatter plot.

Author : Group 8
Version : 4/4/2023

'''


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
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime
import socket

#declaration of variables
counting_factor = count()
hum = []
tem = []
fac = []
new_emails = []
all_emails = []
image_data = []
image_type = []
image_name = []
all_list = []
group_emails = []
png_files = []
new_files_to_be_sent = []
#file paths
PATH1 = r'E:\data_project\data_analysis.csv' #file path to .csv file 
PATH2 = r'E:\data_project'# file path to content folder

fieldnames = ['Humidity','Temperature'] #csv header lines
pattern = re.compile(r'-?\d+\.?\d*') #regular expression
pattern2 = re.compile(r'^.*.{8,}[gmail\.com]$')

# sends mail using smtp lib and attachments with MIME
def SendMail(ImgFileName,receiver_email):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = f'Data Analysis as: {str(datetime.datetime.now())}'
    msg['From'] = "dataanalysisg8@gmail.com "
    msg['To'] = receiver_email

    text = MIMEText("GROUP 8 : data figures & graphs")
    msg.attach(text)
    image = MIMEImage(img_data, name=ImgFileName)
    msg.attach(image)

    
  
    try:
      with smtplib.SMTP(host = 'smtp.gmail.com',port = 587,timeout=30) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("kibwaleianthony@gmail.com", 'sulc oenu zkpc ybkm')#kwgi sbkg wcit hkak # dataanalysisg8@gmail.com  #kibwaleianthony@gmail.com  #sulc oenu zkpc ybkm
        s.sendmail('kibwaleianthony@gmail.com',receiver_email, msg.as_string())
        print('success')
        s.quit()
    except TimeoutError:
      print('problem with local area connection...')
#fetch plotted figures
def get_present_file():
  for file in os.listdir(PATH2):
    stem,base = os.path.splitext(file)
    if base == '.png':
      png_files.append(file)

  return png_files

# prompt gmail accounts
def receive_acc():  
  while True:
    data = input('''Add receiver email  ->  'STOP' to terminate : ''')
    if data != 'Stop' and data !='stop' and data !='STOP' :
      if pattern2.match(data):
        new_emails.append(data)
      else:
        print('Invalid Email')
      
    else:
      return new_emails
      break

group_acc = receive_acc()
#executes
def send_png():
  for item in group_acc:
    group_emails.append(item)
  files_to_be_sent = get_present_file()
  for r in files_to_be_sent:
    new_files_to_be_sent.append(os.path.join(PATH2,r))
    
  for pict in new_files_to_be_sent:
    for eml in group_emails:
      SendMail(pict,eml)




#extract data from csv file
def extract_data(cache_frame_data=False):
  hum_empty_list = []
  tem_empty_list = []
  with open(PATH1,'r') as rf:
    data = csv.reader(rf)
    big_list = list(data)
    for h_t_list in big_list:
      if len(h_t_list) == 0 or h_t_list == ['Humidity', 'Temperature']:
        pass
      else:
        hum_variabs,tem_variabs = float(h_t_list[0]),float(h_t_list[1])
        hum_empty_list.append(hum_variabs)
        tem_empty_list.append(tem_variabs)
  return [hum_empty_list,tem_empty_list]

# time variable with counter object
def generate_time():
  current_time = next(counting_factor)
  fac.append(current_time)
  return fac
  
#plots a live graph from the extracted data
def plot_live_graph(i,cache_frame_data=False):
  try:
    ser = serial.Serial('COM12', 9600)  # Arduino port on device manager, 9600 bauds
    if len(fac) == 0:
      print('reading data ...')
    line = ser.readline().decode('utf-8').strip()
    s = [float(s) for s in pattern.findall(line)]
    hum.append(s[0])
    tem.append(s[1])
    print(line)
    with open (PATH1,'w') as fp:
      writer = csv.DictWriter(fp,fieldnames=fieldnames)
      writer.writeheader()
      for index,value in enumerate(range(len(hum))):
        writer.writerow({'Humidity':hum[index],'Temperature':tem[index]})
        #creates a row of Humidity and Temperature Headlines
          
    variables = extract_data()
    my_time = generate_time()
    humty = variables[0]
    tempr = variables[1]
    flush_time = len(humty)/3
#plots live graph
    if len(my_time) < 100:
      plt.cla()
      plt.plot(my_time,humty,color='red',linewidth=1,linestyle='--',label='Temperature')
      plt.plot(my_time,tempr,color='green',linewidth=1,linestyle='--',label='Humidity')
      plt.xlabel('Time (s)')
      plt.ylabel('Humidity(%) and Temperature (C)')
      plt.legend(loc='upper right')
    if len(my_time) > 100:
      plt.cla()
      plt.plot(my_time[int(round(flush_time)):],humty[int(round(flush_time)):],color='red',linewidth=1,linestyle='--',label='Temperature')
      plt.plot(my_time[int(round(flush_time)):],tempr[int(round(flush_time)):],color='green',linewidth=1,linestyle='--',label='Humidity')
      plt.xlabel('Time (s)')
      plt.ylabel('Humidity(%) and Temperature (C)')
      plt.legend(loc='upper right') 
    if len(humty)%80 == 0:
      humidity_for_pie = np.average(humty)
      temperature_for_pie = np.average(tempr)
      plt.pie([humidity_for_pie,temperature_for_pie],labels=['Humidity (%)','Temperature (C)'])
      plt.savefig(r'E:\data_project\proj_pic_pie.png')
    if len(humty)%90 == 0:
       plt.scatter(my_time,humty,color='red',alpha=0.5)
       plt.scatter(my_time,tempr,color='green')
       plt.savefig(r'E:\data_project\proj_pic_scatter.png')
    if len(humty)%100 == 0:
      print('there')
      send_png()
  except serial.SerialException:
    print('failed to read port ...')
#get current figures then plot the updated graph
ani = FuncAnimation(plt.gcf(),plot_live_graph,interval=2500,cache_frame_data=False)
plt.show()
plt.tight_layout()
plt.style.use('fivethirtyeight')