/* the foolowing code is an improvement of the previous LCD display version of the DHT11 arduino humidity monitoring system
in this code the OLED has replaced the 16x2 LCD since it uses fewer pins , the remaining I/O pins can be used to add more sensors to the system and also more output 
devices */





#include <DHT.h>          //Include the DHT library

#include <SoftwareSerial.h>
#include<SPI.h>
#include<Wire.h>
#include<Adafruit_GFX.h>
#include<Adafruit_SSD1306.h>

#define BT_TX_PIN 9
#define BT_RX_PIN 3
#define DHTPIN 2          //Pin where the DHT11 is connected
#define DHTTYPE DHT11     //Type of DHT sensor
#define screen_width 128
#define screen_height 64
#define OLED_RESET 4

DHT dht(DHTPIN, DHTTYPE);

SoftwareSerial BTSerial( BT_TX_PIN ,BT_RX_PIN); // RX | TX

Adafruit_SSD1306 display(screen_width,screen_height);


void setup() {
  Serial.begin(9600);
          
  dht.begin();              //Initialize the DHT sensor
   display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  
  display.clearDisplay();
}

void loop() {

  delay(2000);  
 // int chk = DHT.read11(DHT11_PIN);            //Wait for 2 seconds
  float temperature = dht.readTemperature();    //Read the temperature from the DHT sensor
  float humidity = dht.readHumidity();  
  
  if (isnan(humidity) || isnan(temperature)) {
 Serial.println("Failed to read from DHT sensor!");
 return;
}        //Read the humidity from the DHT sensor


Serial.print("Humidity: ");
Serial.print(humidity);
Serial.print(" %\t");
Serial.print("Temp: ");
Serial.print(temperature);
Serial.println(" *C");

BTSerial.print("temp: ");
BTSerial.print(temperature);
BTSerial.print((char)223);
BTSerial.print("C");
BTSerial.print(", humidity: ");
BTSerial.print(humidity);
BTSerial.print("%\r\n");


display.clearDisplay();  
   display.setTextSize(1);  
   display.setTextColor(SSD1306_WHITE);  
   display.setCursor(0, 0);  
   display.print("  TEMP. & HUMIDITY");  
   display.setCursor(0, 25);  
   display.print(" TEMPERATURE : ");  
   display.setCursor(85, 25);  
   display.print(temperature);  
   display.setCursor(0, 45);  //50
   display.print(" HUMIDITY  : ");  
   display.setCursor(85, 45);  
   display.print(humidity);  
   display.print("%"); 
   display.display(); 

delay(1000);
}
