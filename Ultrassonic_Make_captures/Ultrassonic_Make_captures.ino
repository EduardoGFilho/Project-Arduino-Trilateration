#include <Ultrasonic.h>

//UltraSonicDistanceSensor distanceSensor(13, 12);  // Initialize sensor that uses digital pins 13 and 12.
Ultrasonic ultrasonic(3);

unsigned long pulseDuration = 0;
bool isEnabled = false;

void serial_flush(void) {
  while (Serial.available()) Serial.read();
}

void setup () {

  Serial.begin(9600);

}

void loop () {

  if (isEnabled)
  {
    for (int i = 0; i< 2; i++)
    {
        Serial.println("");
    }
    for (int i = 0; i < 5; i++)
    {
      // Note: The library was patched to change this functions scope from private to public
      pulseDuration = ultrasonic.timing();
      Serial.println(pulseDuration);
      delay(1000);
    }

    isEnabled = false;

  }
  else {
    while (Serial.available() == 0)
    {
    }
    serial_flush(); // Flush buffer
    isEnabled = true;

  }

}
