#include <DHT.h>          //Include the DHT library
#include <LiquidCrystal.h> //Include the LCD library
#include <SoftwareSerial.h>
#define DHTPIN 2          //Pin where the DHT11 is connected
#define DHTTYPE DHT11     //Type of DHT sensor
DHT dht(DHTPIN, DHTTYPE);
int rs=12;
int en=11;
int d4=7;
int d5=6;
int d6=5;
int d7=4;
LiquidCrystal lcd(rs,en,d4,d5,d6,d7);
int red_led =10;
int green_led =9;
int buzz_pin = 8;
int dt =700;
void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);         //Set the number of columns and rows of the LCD
  dht.begin();               //Initialize the DHT sensor
  pinMode(green_led , OUTPUT);
  pinMode(red_led , OUTPUT);
  pinMode(buzz_pin , OUTPUT);           
}

void loop() {

  // delay(1000);  
  float temperature = dht.readTemperature();    //Read the Temperature from the DHT sensor
  float humidity = dht.readHumidity();         //Read the Humidity from the DHT sensor

  if (temperature> 28 || humidity <30){
    digitalWrite(green_led ,LOW);
    digitalWrite(red_led ,HIGH);
    digitalWrite(buzz_pin ,HIGH);
    delay(dt);
    digitalWrite(red_led , LOW);
    digitalWrite(buzz_pin ,LOW);
    delay(dt);
  }
  else {
    digitalWrite(green_led , HIGH);
    delay(1400);
  }
  
 if (isnan(humidity) || isnan(temperature)) {
 Serial.println("Failed to read from DHT sensor!");
 return;
}       
   //print the humidity and temperature values on the LCD
  lcd.clear();              //Clear the LCD screen
  lcd.setCursor(0, 0);      //Set the cursor to the top-left corner
  lcd.print("Temp: ");      //Print the word "Temp" on the LCD
  lcd.print(temperature);   //Print the temperature value on the LCD
  lcd.print(" C");          //Print the unit of temperature on the LCD
  lcd.setCursor(0, 1);      //Set the cursor to the bottom-left corner
  lcd.print("Humidity: ");  //Print the word "Humidity" on the LCD
  lcd.print(humidity);      //Print the humidity value on the LCD
  lcd.print("%");           //Print the unit of humidity on the LCD

Serial.print("Temperature: ");
Serial.print(temperature);
Serial.print(" *C \t");
Serial.print("Humidity: ");
Serial.print(humidity);
Serial.println("%");
}