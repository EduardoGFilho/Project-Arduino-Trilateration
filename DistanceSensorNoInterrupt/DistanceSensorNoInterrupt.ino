byte lastPORTD = B00000000;

unsigned long startMicros = 0;
unsigned long pulseDuration = 0;

#define echoIn 3//2 // In process of inverting echoIn and activate
#define activate 2//3
#define TpIn 4
#define TmIn 5

#define speedOfSound 340.29 // m/s

// Constants for the pulsing, must be matched to the other pin assignments

#define setTpIn PORTD |= (1 << PORTD4) //PORTD |= B00001000
#define resetTpIn PORTD &= ~(1 << PORTD4) //PORTD &= B11110111

#define setTmIn PORTD |= (1 << PORTD5) //PORTD |= B00010000
#define resetTmIn PORTD &= ~(1 << PORTD5) //PORTD &= B11101111

#define resetActivate PORTD &= ~(1 << PORTD2) //PORTD &= B11011111 // This doesn't even change but let's keep it

#define resetAll PORTD &= ~( (1 << PORTD2) & (1 << PORTD4) & (1 << PORTD5) ) // Resets TpIn, Tmin and Activate 

float timeOfFlight = 0.0;
float measuredDistance = 0.0;

// Counter
unsigned long i = 0;

// Prototypes

unsigned long readDistance();
void sendPulse();

void setup()
{
  // Set pin modes
  pinMode(echoIn, INPUT);
  pinMode(activate, OUTPUT);
  pinMode(TpIn, OUTPUT);
  pinMode(TmIn, OUTPUT);

  // Make a voltimeter cause i aint got one
  pinMode(A4, INPUT);


  // Serial
  Serial.begin(9600);

}


void loop()
{
  Serial.println(analogRead(A4)*5.0/1023);
  timeOfFlight = (float)(readDistance());
  measuredDistance = timeOfFlight * 0.5 * 1e-6 / speedOfSound; // meters

  //Serial.print("Distance (m):");
  //Serial.println(measuredDistance);
  delay(500);

}

// Anytime we want to change pin assignments, we gotta change the binary words here
// since digitalRead/digitalWrite are too slow

// This implementation blocks the code
unsigned long readDistance()
{
  // Start the reading
  sendPulse(); // Send pulse, this blocks for a while
  startMicros = micros(); // Start counting from trig

  // Look for an edge in echoIn
  lastPORTD = PORTD;

  // TODO: Implement a timeout
  // Only evaluates to true when there's a change in PORTD3, our echoIn
  while ( ( (~(PORTD ^ lastPORTD)) & (1 << PORTD3) ))
  {
    lastPORTD = PORTD;
    i++;

    // Time out
    if (micros() - startMicros > 1000)
    {
      return 999999;
    }
    //delayMicroseconds(5);
  }


  // Measure time
  pulseDuration = micros() - startMicros;



  return pulseDuration;

}


void sendPulse()
{
  delayMicroseconds(150);
  /*We have seen a delay of 250uS when we've made tests
    between the 10us trig pulse and the 8 cycles burt. For some reasons, if I put 250us delay,
    I get 350 on the oscilloscope. That's why I've made a 150us delay.
  */
  resetActivate;

  setTpIn;
  resetTmIn;
  delayMicroseconds(12); // 12us so around 40KHz. Freq = 1/2*12us
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);
  // We do this 8 times...
  setTpIn;
  resetTmIn;
  delayMicroseconds(12);
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);

  setTpIn;
  resetTmIn;
  delayMicroseconds(12);
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);

  setTpIn;
  resetTmIn;
  delayMicroseconds(12);
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);

  setTpIn;
  resetTmIn;
  delayMicroseconds(12);
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);

  setTpIn;
  resetTmIn;
  delayMicroseconds(12);
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);

  setTpIn;
  resetTmIn;
  delayMicroseconds(12);
  resetTpIn;
  setTmIn;
  delayMicroseconds(12);

  setTpIn;
  resetTmIn;
  delayMicroseconds(12);

  resetAll; // D3, D4, D5 LOW  //We have finished the burst. We set everything to low

}
