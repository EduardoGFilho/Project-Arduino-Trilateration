#include <DHT.h>
#include <TM1637Display.h>
#include <SoftwareSerial.h>
#define DHTPIN 4
#define DHTTYPE DHT11
#define BUTTONPIN 3

#define BLUETOOTHPIN1 0
#define BLUETOOTHPIN2 1

float temp = 0;
float hum = 0;
float maxTemp = temp;
float maxHum = hum;

float lastTemp = 0;
float lastHum = 0;

int tempD1 = 0;
int tempD2 = 0;

TM1637Display display(6,7); // CLK, DIO
DHT dht(DHTPIN,DHTTYPE);
SoftwareSerial bluetooth(BLUETOOTHPIN1, BLUETOOTHPIN2); //RX, TX

void setup() {
  //Serial.begin(9600);
  pinMode(BUTTONPIN, INPUT);
  display.setBrightness(4);
  display.clear();

  Serial.begin(9600); 
  bluetooth.begin(9600); 

}

void loop() {

  maxTemp = 88;

  temp = dht.readTemperature();
  if (isnan(temp))
  {
    temp = lastTemp;
  }
  else
  {
    lastTemp = temp;  
  }

  hum = dht.readHumidity();
  
    if (isnan(hum))
  {
    hum = lastHum;
  }
  else
  {
    lastHum = hum; 
  }
  

  int tempInt = (int)(temp + 0.5);
  int maxTempInt = (int)(maxTemp + 0.5);
  //Serial.println(tempInt);

  //tempInt = 94;

  display.clear();
  //display.showNumberDec(2, true,tempD1, tempD2);
  //display.showNumberDec(tempInt, false);

  
  if(temp > maxTemp)
  {
    maxTemp = temp;
  }
    if(hum > maxTemp)
  {
    maxTemp = temp;
  }
  
  bool isButtonPressed = (digitalRead(BUTTONPIN) == HIGH);
  if(isButtonPressed)
  {
    display.showNumberDec(maxTempInt, false);
    Serial.println("Maximum Temperature = " + String(maxTemp));
    Serial.println("Maximum Humidity = " + String(maxHum));
    }
    
  else
  {  
    display.showNumberDec(tempInt, false);
    Serial.println("Temperature = " + String(temp));
    Serial.println("Humidity = " + String(hum));
  }
  
  bluetooth.print(temp);  
  bluetooth.print(";");  
  Serial.println(hum);  
  
  delay(500);

}
