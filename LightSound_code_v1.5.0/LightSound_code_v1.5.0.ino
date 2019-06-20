/* Developed for the LightSound 2.0 */
/* Code developed by Soley Hyman, with help from Daniel Davis, Rob Hart, and Keith Crouch */
/* last updated: 2 May 2019 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_TSL2591.h>
#include <SoftwareSerial.h>

/**************************************************************************/
// define the pins used
#define VS1053_RX  10 // This is the pin that connects to the RX pin on VS1053
#define VS1053_RESET 9 // This is the pin that connects to the RESET pin on VS1053
// Don't forget to connect the GPIO #0 to GROUND and GPIO #1 pin to 3.3V

// define MIDI channel messages
// See http://www.vlsi.fi/fileadmin/datasheets/vs1053.pdf Pg 31
#define VS1053_BANK_DEFAULT 0x00 // default bank
#define VS1053_BANK_DRUMS1 0x78  // drums bank (unnecessary?)
#define VS1053_BANK_DRUMS2 0x7F  // drums bank (unnecessary?)
#define VS1053_BANK_MELODY 0x79  // melodic bank
#define VS1053_RPN_MSB 0x06 // most sig. bit for bend/coarse tune
#define VS1053_RPN_LSB 0x26 // leas sig. bit for bend

// define MIDI sounds
// See http://www.vlsi.fi/fileadmin/datasheets/vs1053.pdf Pg 32 for more!
#define VS1053_GM1_SQUARE_CLICK 32 // square click
#define VS1053_GM1_CLARINET 72 // clarinet sound
#define VS1053_GM1_FLUTE 74 // flute sound
#define VS1053_GM1_WOODBLOCK 116 // woodblock sound
#define VS1053_GM1_ACOUSTICBASS 33 // acoustic bass

// more channel messages
#define MIDI_NOTE_ON  0x90     // note on
#define MIDI_NOTE_OFF 0x80     // note off
#define MIDI_CHAN_MSG 0xB0     // parameter (not sure what this does)
#define MIDI_CHAN_BANK 0x00    // calling in the default bank?
#define MIDI_CHAN_VOLUME 0x07  // channel volume
#define MIDI_CHAN_PROGRAM 0xC0 // program (not sure exactly what this does)
#define MIDI_CHAN_PITCH_WHEEL 0xE0 //pitch wheel

// might be old code from color arduino? maybe not functioning
// we only play a note when the clear response is higher than a certain number 
//#define CLEARTHRESHHOLD 2000 
#define CLEARTHRESHHOLD 100 // threshhold from color arduino? not sure if function
#define LOWTONE 1000
#define HIGHTONE 2000
#define LOWKEY 40 // use this - two octaves lower than high C?
//#define LOWKEY 52   // octave lower than high C? 
//#define LOWKEY 64   // high C
#define HIGHKEY 76  // double high C
// not sure the difference between 'tone' and 'key'

// defines way of looking at previous note
int prevNote = -1;

/**************************************************************************/
// variables from eclipse arduino code -- not sure what is relevant to LightSound
// some for publishing to web?
int SwitchState=0; //Variable to store state of switch to publish to web or just play audio
int SwitchStatePin=12; //Pin to publish to web (high/on), or just play audio (low/off)
int TonePin=13; //Pin to play tone output
int LedPin=0; //Pin to light LED indicator (0 on ESP8266 breakout)
int PinState=LOW; //Variable to store state of tone/led pin
unsigned long previousMicros; //stores last time tone/led pin was updated
unsigned long OnTime=100; //microseconds on-time
unsigned long OffTime=100; //microseconds off-time
unsigned long previousMillis; //stores last time light sensor was read
unsigned long ReadTime=2000; //Light sensor read interval in milliseconds
float lvl=0.0;
int noteCase=0;
int prevLvlInt=0; 
float prevLvl=0.0; 
float delayTime=0.0;
int lvlInt=0;
int delayTimeInt=0;
uint32_t x=0;
uint16_t ir=0; //infrared sensor value 16 bit
uint16_t full=0; //full spectrum sensor value 16 bit 
uint16_t vis=0;  //visible spectrum inferred from full spectrum and IR sensors
uint32_t lum=0; //32 bit full spectrum MSB's, IR LSB's

// variable to hold sensor value
int sensorValue;
// variable to calibrate low value; use bigger number for lower value to invert dependencece
int sensorLow = 0; 
// variable to calibrate high value; note A2D converter is 10 bit, so max is 1023
int sensorHigh = 32767; 
//131072, 65353 (both as unsigned longs) 32767 (int) stack errors on serial monitor; even using constrain to convert float lvl to int
int pitchLow = 1; //Note minimum pitch for tone function is 31Hz; manually write high/low to get lower pitches
int pitchHigh = 10000; //Note I can only hear up to just above 10kHz
int waitLow = 1; //wait time lower bound
int waitHigh = 16383; //wait time upper bound for delayMicroseconds()
//int sensorPin = A5; //Adafruit Circuit Playground light sensor pin (phototransistor)
int wait = 0; //wait time 
int ncycles = 10; //number of times to toggle pin
int nwait = 0; //wait factor multiplier
int nwaitLow = 0;
int nwaitHigh = 200;

/**************************************************************************/
// lux sensor setup
Adafruit_TSL2591 tsl = Adafruit_TSL2591(2591); // TSL2591 Lux sensor
SoftwareSerial VS1053_MIDI(0, VS1053_RX); //MIDI board; TX only, do not use the 'rx' side

/**************************************************************************/
// define setup loop
void setup() {
  
  Serial.begin(9600); // serial rate of some type?
  Serial.println("Lux Sensor MIDI!");

  //Check for light sensor (loop with error print-out)
  if (tsl.begin()) {
    Serial.println("Found sensor");
  } 
  else {
    Serial.println("No TSL2561 found ... check your connections");
    while (1); // halt!
  }

  //Start VS1053 module
  VS1053_MIDI.begin(31250); // MIDI uses a 'strange baud rate'
  
  //Resetting the VS1053 board before using it
  pinMode(VS1053_RESET, OUTPUT);    // Set the VS1053 assigned pin as Digital Output
  digitalWrite(VS1053_RESET, LOW);  // Reset VS1053 module by shorting the reset pin to the ground
  delay(10);                        // Waiting a bit while the reset is being performed
  digitalWrite(VS1053_RESET, HIGH); // Stop shorting the pin (sending 3.3v)
  delay(10);                        // Waiting again before initialize the module
  
  // Initialize MIDI
  midiSetChannelBank(0, VS1053_BANK_MELODY); // sets melody channel for MIDI board
  midiSetInstrument(0, VS1053_GM1_CLARINET); // sets clarinet sound for MIDI instrument
  midiSetChannelVolume(0, 127);              // sets volume -- able to change volume
}

/**************************************************************************/
/**************************************************************************/
 /****** light sensor config function definitions ******/
/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  tsl.getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.print  (F("Sensor:       ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:   ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:    ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:    ")); Serial.print(sensor.max_value); Serial.println(F(" lux"));
  Serial.print  (F("Min Value:    ")); Serial.print(sensor.min_value); Serial.println(F(" lux"));
  Serial.print  (F("Resolution:   ")); Serial.print(sensor.resolution); Serial.println(F(" lux"));  
  Serial.println(F("------------------------------------"));
  Serial.println(F(""));
  delay(500);
//  delay(1000); //Delay to ensure time between readouts given max 400ms integration time; AND to stay below Adafruit IO throttle rate 125 posts in 60 seconds
}

/**************************************************************************/
/*
    Configures the gain and integration time for the TSL2561
*/
/**************************************************************************/
void configureSensor(void)
{
  /* You can also manually set the gain or enable auto-gain support */
  //tsl.setGain(TSL2591_GAIN_LOW);    /* 1x gain (bright light) */
  //tsl.setGain(TSL2591_GAIN_MED);    /* 25x gain */
  //tsl.setGain(TSL2591_GAIN_HIGH);   /* 428x gain */
  tsl.setGain(TSL2591_GAIN_MAX);      /* 9876x gain (extremely low light) */
  
  /* Changing the integration time gives you a longer time over which to sense light */
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);  // shortest integration time (bright light)
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_200MS);
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_300MS);
  tsl.setTiming(TSL2591_INTEGRATIONTIME_400MS);    /* closest to the 402 ms used for TSL2561 version */
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_500MS);
  //tsl.setTiming(TSL2591_INTEGRATIONTIME_600MS);  // longest integration time (dim light)

  /* Update these values depending on what you've set above! */  
  Serial.println("------------------------------------");
  Serial.print  ("Gain:         "); Serial.println("Auto");
  Serial.print  ("Timing:       "); Serial.println("402 ms");
  Serial.println("------------------------------------");

/**************************************************************************/
/**************************************************************************/

  /* Display some basic information on this sensor */
  displaySensorDetails();
  
  /* Setup the sensor gain and integration time */
  configureSensor();
  
  /* We're ready to go! */
  Serial.println("");
}

/**************************************************************************/      
// Performs a read using the Adafruit Unified Sensor API. 
/**************************************************************************/
// loop for reading with Lux sensor

void loop(){
  /* Get a new sensor event */ 
  lvl = advancedLightSensorRead();
  
  /* Play the corresponding note to the lux */
   advancedPlayNoteBending(lvl);
}


/**************************************************************************/      
// Function defintions
/**************************************************************************/
/* definition for measurement/autogain function*/
float advancedLightSensorRead(void)
{

  // auto gain from http://microcontrolbasics.blogspot.com/2015/04/adafruit-tsl2591-lux-sensor.html
  // More advanced data read example. Read 32 bits with top 16 bits IR, bottom 16 bits full spectrum
  // That way you can do whatever math and comparisons you want!
  
  sensors_event_t event;
  tsl.getEvent(&event);

  lvl = event.light;

  Serial.print(F("[ ")); Serial.print(millis()); Serial.print(F(" ms ] ")); Serial.println(F("  "));
  Serial.print(F("Visible (event.light): ")); Serial.print(event.light); Serial.print(F(" Lux ")); Serial.println(F(" "));

   
  if (event.light <= 0)
  {
    tsl.setGain(TSL2591_GAIN_LOW);              
    tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);
    Serial.println("Gain: 1x (Low)");
    Serial.println("Integration: 100 ms");
  }
  else if (event.light > 200.0)
  { 
    tsl.setGain(TSL2591_GAIN_LOW);              
    tsl.setTiming(TSL2591_INTEGRATIONTIME_100MS);
    Serial.println("Gain: 1x (Low)");
    Serial.println("Integration: 100 ms");
  }
  else if (event.light <=200.0 && event.light > 40.0)
  {
    tsl.setGain(TSL2591_GAIN_MED);                
    tsl.setTiming(TSL2591_INTEGRATIONTIME_200MS);
    Serial.println("Gain: 25x (Med)");
    Serial.println("Integration: 200 ms");
  }
  else if (event.light <=40.0 && event.light > 10.0)
  {
    tsl.setGain(TSL2591_GAIN_MED);                
    tsl.setTiming(TSL2591_INTEGRATIONTIME_600MS);
    Serial.println("Gain: 25x (Med)");
    Serial.println("Integration: 600 ms");
  }
  else if (event.light <=10.0 && event.light > 0.1)
  {
    tsl.setGain(TSL2591_GAIN_HIGH);                
    tsl.setTiming(TSL2591_INTEGRATIONTIME_600MS);
    Serial.println("Gain: 428x (High)");
    Serial.println("Integration: 600 ms");
  }
  else
  {
    tsl.setGain(TSL2591_GAIN_MAX);                
    tsl.setTiming(TSL2591_INTEGRATIONTIME_600MS);
    Serial.println("Gain: 9876x (Max)");
    Serial.println("Integration: 600 ms");
  }
  Serial.println(" ");

  prevLvl = lvl;
  return lvl;
 
}

/* *********** */

// definition for "play note" function
void advancedPlayNoteBending(float lvl) {
  if (lvl < 61 & lvl >= 0){
    //stop last note played
    if (noteCase == 1) {
      midiNoteOff(0, prevNote, 100);
    }

    else if (noteCase == 2) {
      midiNoteOff(0, prevNote, 62);
    }

    lvlInt = round(lvl);
    delayTime = 1000/lvl;
    delayTimeInt = round(delayTime);

    midiSetChannelBank(0, VS1053_BANK_DRUMS1);
    midiSetInstrument(0, VS1053_GM1_SQUARE_CLICK);

    if (lvlInt > 0) {
      for (int count = 0; count < lvlInt; count++) {
        midiNoteOn(0, 69, 127);
        delay(5);
        midiNoteOff(0, 69, 127);
        delay(delayTimeInt);
      }
    }

    else if (lvlInt == 0 & lvl > 0){
      midiNoteOn(0, 69, 127);
      delay(5);
      midiNoteOff(0, 69, 127);
      delay(2000);
    }
   
   noteCase = 0;
   prevLvlInt = lvlInt;
  }

  else if (lvl >= 61) {
    if (lvl <= 10000) {
      float nFloat = mapfloat(lvl,61,10000,35,81);
      
      //extract decimal
      int nInt = nFloat;
      String stringval = String(nFloat);
      String mantissa = stringval.substring(stringval.lastIndexOf(".") + 1, stringval.lastIndexOf(".") + 2);
      int decimalInt = mantissa.toInt();
      int decMap = map(decimalInt,0,10,8192,16383);        

      if (nInt == prevNote & noteCase == 1) return;
    
      if (nInt == -1 & noteCase == 1){
        midiNoteOff(0, prevNote, 100);
      }

      else if (nInt == -1 & noteCase == 2){
        midiNoteOff(0, prevNote, 62);
      }
    
      //stop last note played
      if (noteCase == 1){
        midiNoteOff(0, prevNote, 100);
      }

      else if (noteCase == 2){
        midiNoteOff(0, prevNote, 62);
      }

      //play new note with bend
      midiSetChannelBank(0, VS1053_BANK_MELODY);
      midiSetInstrument(0, VS1053_GM1_CLARINET);
      midiNoteOn(0, nInt, 100);
      pitchBendChange(0,decMap);     

      prevNote = nInt;
      noteCase = 1;
    }
    
    else {   
      float nHighFloat = mapfloat(lvl,10000,131072,81,90);
      
      //extract decimal
      int nHighInt = nHighFloat;
      String stringvalHigh = String(nHighFloat);
      String mantissaHigh = stringvalHigh.substring(stringvalHigh.lastIndexOf(".") + 1, stringvalHigh.lastIndexOf(".") + 2);
      int decimalIntHigh = mantissaHigh.toInt();
      int decMapHigh = map(decimalIntHigh,0,10,8192,16383);

      if (nHighInt == prevNote & noteCase == 2) return;
   
      if (nHighInt == -1 & noteCase == 1){
        midiNoteOff(0, prevNote, 100);
      }

      else if (nHighInt == -1 & noteCase == 2){
        midiNoteOff(0, prevNote, 62);
      }

      if (noteCase == 1){
        midiNoteOff(0, prevNote, 100);
      }

      else if (noteCase == 2){
        midiNoteOff(0, prevNote, 62);
      }
      
      midiSetChannelBank(0, VS1053_BANK_MELODY);
      midiSetInstrument(0, VS1053_GM1_FLUTE);
      midiNoteOn(0, nHighInt, 62);
      pitchBendChange(0,decMapHigh);
      delay(500);

      prevNote = nHighInt;
      noteCase = 2;
    } 
  }

  else if (lvl < -5){
    if (noteCase == 1){
        midiNoteOff(0, prevNote, 100);
      }

    if (noteCase == 2){
        midiNoteOff(0, prevNote, 62);
      }

    midiSetChannelBank(0, VS1053_BANK_MELODY);
    midiSetInstrument(0, VS1053_GM1_ACOUSTICBASS);

    midiNoteOn(0, 90, 88);
    pitchBendChange(0,8192);
    delay(500);
    midiNoteOff(0, 90, 88);
    delay(1000);
    noteCase = 3;
    
  }
}


// definition for float map function 
// from: https://forum.arduino.cc/index.php?topic=3922.0 (post #2)
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max){
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
 

/*
 * micros() overflows in ~70 minutes; 4us resolution
 * millis() overflows in ~50 days
 * 
 * light level ranges from 1/24th to 65,536*2=131072; Range is 131072*24=3,145,728
 * sound level ranges from 0.1 Hz to 10kHz; Range is ~10^5
 * 
 * avoiding fractions requires dealing with periods rather than frequencies
 * resolution limited to integer changes in milliseconds (1ms) or 4us micros() resolution
 * 0.1Hz-10kHz -> 100ms-100usec
 * weight lower light level range; compress upper light level range
 */
/**************************/

// definition for MIDI instrument function
void midiSetInstrument(uint8_t chan, uint8_t inst) {
  if (chan > 15) return;
  inst --; // page 32 has instruments starting with 1 not 0 :(
  if (inst > 127) return;
  
  VS1053_MIDI.write(MIDI_CHAN_PROGRAM | chan);  
  VS1053_MIDI.write(inst);
}

// definition for MDID volume function
void midiSetChannelVolume(uint8_t chan, uint8_t vol) {
  if (chan > 15) return;
  if (vol > 127) return;
  
  VS1053_MIDI.write(MIDI_CHAN_MSG | chan);
  VS1053_MIDI.write(MIDI_CHAN_VOLUME);
  VS1053_MIDI.write(vol);
}

// definition for MIDI bank function (i.e. default v.s. drums v.s. melodic?)
void midiSetChannelBank(uint8_t chan, uint8_t bank) {
  if (chan > 15) return;
  if (bank > 127) return;
  
  VS1053_MIDI.write(MIDI_CHAN_MSG | chan);
  VS1053_MIDI.write((uint8_t)MIDI_CHAN_BANK);
  VS1053_MIDI.write(bank);
}

// definition for MIDI "note on" function
void midiNoteOn(uint8_t chan, uint8_t n, uint8_t vel) {
  if (chan > 15) return;
  if (n > 127) return;
  if (vel > 127) return;
  
  VS1053_MIDI.write(MIDI_NOTE_ON);
  VS1053_MIDI.write(n);
  VS1053_MIDI.write(vel);
}

// definition for MIDI "note off" function
void midiNoteOff(uint8_t chan, uint8_t n, uint8_t vel) {
  if (chan > 15) return;
  if (n > 127) return;
  if (vel > 127) return;
  
  VS1053_MIDI.write(MIDI_NOTE_OFF | chan);
  VS1053_MIDI.write(n);
  VS1053_MIDI.write(vel);
}

// definition for MIDI "note bend" function

/* from: https://arduino.stackexchange.com/questions/18955/how-to-send-a-pitch-bend-midi-message-using-arcore
   The pitch bend value is a 14-bit number (0-16383). 0x2000 (8192) is the default / middle value.
   First byte is the event type (0x0E = pitch bend change).
   Second byte is the event type, combined with the channel.
   Third byte is the 7 least significant bits of the value.
   Fourth byte is the 7 most significant bits of the value. */

void pitchBendChange(byte channel, int value) {
  byte lowValue = value & 0x7F;
  byte highValue = value >> 7;
  VS1053_MIDI.write(0xE0 | channel);
  VS1053_MIDI.write(lowValue);
  VS1053_MIDI.write(highValue);
}
