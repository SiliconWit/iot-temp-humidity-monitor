import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
import re
import PIL
import csv
ser = serial.Serial('COM5', 9600)  # Replace 'COM#' with the appropriate port number
time.sleep(2)
PATH = r'C:\Users\SEVENS\data_analysis.csv'
fieldnames = ['Humidity','Temperature']
pattern = re.compile(r'-?\d+\.?\d*')
hum = []
tem = []
while True:
  line = ser.readline().decode('utf-8').strip()
  time.sleep(2)
  s = [float(s) for s in pattern.findall(line)]
  hum.append(s[0])
  tem.append(s[1])
  print(line)
  with open (PATH,'w') as fp:
    writer = csv.DictWriter(fp,fieldnames=fieldnames)
    writer.writeheader()
    for index,value in enumerate(range(len(hum))):
      writer.writerow({'Humidity':hum[index],'Temperature':tem[index]})
