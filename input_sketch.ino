#include "Led.h"
#include <CapacitiveSensor.h>
#include "Capacitor.h"
//CapacitiveSensor cap_sens1 = CapacitiveSensor(4,2);
//CapacitiveSensor cap_sens2 = CapacitiveSensor(9, 10);

const int buttonPin = 7;     // the number of the pushbutton pin
const int ledPin_notifications=8;
const int ledPin_recording=6;
//const int ledPin_cap2=11;

// variables will change:
int prevButtonState = 0;
int buttonState = 0;         // variable for reading the pushbutton status

unsigned nots = 0;
//const int numReadings = 10;
//
//int readings[numReadings];      // the readings from the analog input
//int index = 0;                  // the index of the current reading
//int total = 0;                  // the running total
//int average = 0;                // the average

boolean recording = false;

const unsigned rec_cap_thresh = 200;
const unsigned playback_cap_thresh = 180;

Capacitor rec_cap(4, 2, rec_cap_thresh);
Capacitor playback_cap(5, 3,  playback_cap_thresh);

Led rec_led(ledPin_recording,50,100);
Led nots_led(ledPin_notifications,1000,1000);

//Led previous(ledPin_cap2,1000,1000);

void setup(){
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  prevButtonState = digitalRead(buttonPin);
}

void loop()
{
  //  //SMOOTHING FOR BOTH SENSORS
  //  // subtract the last reading:
  //  total= total - readings[index];         
  //  // read from the sensor:  
  //  readings[index] = cap_sens1.capacitiveSensor(30); 
  //  //readings[index] = cap_sens2.capacitiveSensor(30); 
  //  // add the reading to the total:
  //  total= total + readings[index];       
  //  // advance to the next position in the array:  
  //  index = index + 1;                    
  //  // if we're at the end of the array...
  //  if (index >= numReadings)              
  //    // ...wrap around to the beginning: 
  //    index = 0;                           
  //  // calculate the average:
  //  cap_value1 = total / numReadings;   
  //  cap_value2 = total / numReadings;   
  //  //  
  //  // cap_value2 =  cap_sens2.capacitiveSensor(30);
  //  if (!touching1 && cap_value1 > cap_thresh){
  //    touching1 = true;
  //  }
  //  else if (touching1 && cap_value1 < cap_thresh){
  //    //button has been pressed
  //    touching1 = false;
  //    if (recording1){
  //      stopRecording();
  //    }
  //    else if (!recording1){
  //      startRecording();
  //    }
  //  }
  //Serial.print(rec_cap.getValue());
  //Serial.print("\t");
  //Serial.println(playback_cap.getValue());

  if (rec_cap.wasPressed()){
    if (recording){
      stopRecording();
    }
    else{
      startRecording();
    }
  }
  if (playback_cap.wasPressed()){
    Serial.println(3);
  }
  checkBtnPress();
  handleLeds();

}
//////////////////////////////////////////////////////
void startRecording(){
  recording = true;
  if (!rec_led.isBlinking()){
    rec_led.startBlink();
  }
  Serial.println(1);
}

void stopRecording(){
  recording = false;
  if (rec_led.isBlinking()){
    rec_led.stopBlink();
  }
  Serial.println(4);
  nots_led.startBlink();
  nots++;

} 
void checkBtnPress(){
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH && prevButtonState == LOW){
    if (nots>0){
      nots--;
    }
    Serial.println(2);
    if (nots == 0){
      nots_led.stopBlink();
    }
  }
  prevButtonState = digitalRead(buttonPin);
}

void handleLeds(){
  rec_led.doBlink();
  if (nots>0)
    nots_led.doBlink();
}



//void turnOncap2(){
//  // goPrevious = true;
//  if (!previous.isBlinking()){
//    previous.startBlink();
//  }
//  Serial.println(3);
//}
//
//void turnOffcap2(){
//  // goPrevious = false;
//  if (previous.isBlinking()){
//    previous.stopBlink();
//  }
//  Serial.println(4);
//
//}
//
//void handleLeds2(){
//  previous.doBlink();
//}




