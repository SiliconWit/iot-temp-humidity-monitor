import serial
import time
import pandas as pd
import matplotlib.pyplot as plt

ser = serial.Serial('COM#', 9600)  # Replace 'COM#' with the appropriate port number
time.sleep(2)

data = {"Time": [], "Temperature": [], "Humidity": []}

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if "Temperature" in line and "Humidity" in line:
            parts = line.split('\t')
            humidity = float(parts[0].split(': ')[1])
            temperature = float(parts[1].split(': ')[1])

            data["Time"].append(time.time())
            data["Temperature"].append(temperature)
            data["Humidity"].append(humidity)

except KeyboardInterrupt:
    ser.close()

df = pd.DataFrame(data)
df.to_csv('temp_humidity_data.csv', index=False)

plt.figure()
df.plot(x='Time', y=['Temperature', 'Humidity'])
plt.xlabel('Time (s)')
plt.ylabel('Temperature (C) / Humidity (%)')
plt.title('Temperature and Humidity Monitoring')
plt.legend(['Temperature', 'Humidity'])
plt.show()
