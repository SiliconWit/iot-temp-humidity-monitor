#include <DHT.h>          //Include the DHT library
#include <LiquidCrystal.h> //Include the LCD library
#include <SoftwareSerial.h>
#define BT_TX_PIN 9
#define BT_RX_PIN 3
#define DHTPIN 2          //Pin where the DHT11 is connected
#define DHTTYPE DHT11     //Type of DHT sensor
DHT dht(DHTPIN, DHTTYPE);
int rs=12;
int en=11;
int d4=7;
int d5=6;
int d6=5;
int d7=4;
SoftwareSerial BTSerial( BT_TX_PIN ,BT_RX_PIN); // RX | TX
LiquidCrystal lcd(rs,en,d4,d5,d6,d7);

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);
  lcd.begin(16, 2);         //Set the number of columns and rows of the LCD
  dht.begin();              //Initialize the DHT sensor
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
  lcd.clear();              //Clear the LCD screen
  lcd.setCursor(0, 0);      //Set the cursor to the top-left corner
  lcd.print("Temp: ");      //Print the word "Temp" on the LCD
  lcd.print(temperature);   //Print the temperature value on the LCD
  lcd.print(" C");          //Print the unit of temperature on the LCD
  lcd.setCursor(0, 1);      //Set the cursor to the bottom-left corner
  lcd.print("Humidity: ");  //Print the word "Humidity" on the LCD
  lcd.print(humidity);      //Print the humidity value on the LCD
  lcd.print("%");           //Print the unit of humidity on the LCD

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

delay(1000);
}
