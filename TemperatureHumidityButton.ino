#include <DHT.h>
#include <TM1637Display.h>
#include <SoftwareSerial.h>
#define DHTPIN 4
#define DHTTYPE DHT11
#define BUTTONPIN 9

#define BLUETOOTHPIN1 10
#define BLUETOOTHPIN2 11



float temp = 0;
float hum = 0;
float maxTemp = temp;
float maxHum = hum;

float lastTemp = 0;
float lastHum = 0;

int tempD1 = 0;
int tempD2 = 0;

TM1637Display display(2,3);
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

  //tempInt = 94;

  display.clear();
  //display.showNumberDec(2, true,tempD1, tempD2);
  display.showNumberDec(tempInt, false,2,0);

  
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
    Serial.println("Maximum Temperature = " + String(maxTemp));
    Serial.println("Maximum Humidity = " + String(maxHum));
    }
    
  else
  {  
    
    Serial.println("Temperature = " + String(temp));
    Serial.println("Humidity = " + String(hum));
  }
  
  bluetooth.print(temp);  
  bluetooth.print(";");  
  Serial.println(hum);  
  
  delay(500);

}
