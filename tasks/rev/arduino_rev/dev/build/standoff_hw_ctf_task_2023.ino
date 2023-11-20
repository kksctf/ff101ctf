/**
   Mini piano for Arduino.

   You can control the colorful buttons with your keyboard:
   After starting the simulation, click anywhere in the diagram to focus it.
   Then press any key between 1 and 8 to play the piano (1 is the lowest note,
   8 is the highest).

   Copyright (C) 2021, Uri Shaked. Released under the MIT License.
*/

#include "pitches.h"

#define SPEAKER_PIN 8






#define rest    -1
uint8_t buttonPrev[] = { 0, 0, 0, 0, 0, 0, 0};
const uint8_t buttonPins[] = { 12, 11, 10, 9, 7, 6, 5};
const int buttonTones[] = {
  NOTE_GS4, NOTE_AS4, NOTE_C5, NOTE_CS5,
  NOTE_DS5, NOTE_F5, NOTE_FS5
};


int melody[] =
{ NOTE_AS4, NOTE_AS4, NOTE_GS4, NOTE_GS4,
  NOTE_F5, NOTE_F5, NOTE_DS5, NOTE_AS4, NOTE_AS4, NOTE_GS4, NOTE_GS4, NOTE_DS5, NOTE_DS5, NOTE_CS5, NOTE_C5, NOTE_AS4,
  NOTE_CS5, NOTE_CS5, NOTE_CS5, NOTE_CS5,
  NOTE_CS5, NOTE_DS5, NOTE_C5, NOTE_AS4, NOTE_GS4, NOTE_GS4, NOTE_GS4, NOTE_DS5, NOTE_CS5,
  NOTE_AS4, NOTE_AS4, NOTE_GS4, NOTE_GS4,
  NOTE_F5, NOTE_F5, NOTE_DS5, NOTE_AS4, NOTE_AS4, NOTE_GS4, NOTE_GS4, NOTE_GS5, NOTE_C5, NOTE_CS5, NOTE_C5, NOTE_AS4,
  NOTE_CS5, NOTE_CS5, NOTE_CS5, NOTE_CS5,
  NOTE_CS5, NOTE_DS5, NOTE_C5, NOTE_AS4, NOTE_GS4, rest, NOTE_GS4, NOTE_DS5, NOTE_CS5, rest
};


int rhythmn[] =
{ 1, 1, 1, 1,
  3, 3, 6, 1, 1, 1, 1, 3, 3, 3, 1, 2,
  1, 1, 1, 1,
  3, 3, 3, 1, 2, 2, 2, 4, 8,
  1, 1, 1, 1,
  3, 3, 6, 1, 1, 1, 1, 3, 3, 3, 1, 2,
  1, 1, 1, 1,
  3, 3, 3, 1, 2, 2, 2, 4, 8, 4
};

volatile int beatlength = 100; // determines tempo
float beatseparationconstant = 0.3;

const int numTones = sizeof(buttonPins) / sizeof(buttonPins[0]);
const uint8_t flag[] = {0x2f,0x37,0x32,0x34,0x2e,0x21,0x7e,0x11,0x2f,0x74,0x3f,0x65,0x37,0x11,0x22,0x66,0x2f,0x29,0x7b,0x11,0x29,0x28,0x31,0x7a,0x09,0x3c,0x7e,0x30,0x09,0x34,0x37};
const uint8_t mask[] = {0x4e,0x45,0x56,0x41,0x47,0x4f,0x4e,0x4e,0x41,0x47,0x49,0x56,0x45,0x4e,0x45,0x56,0x41,0x47,0x4f,0x4e,0x4e,0x41,0x47,0x49,0x56,0x45};

int b; // song index
boolean success = false;
boolean finished = false;

int step = 0;
int j = 0;

void blink_correct(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(50); // Wait for 1000 millisecond(s)
  digitalWrite(LED_BUILTIN, LOW);
  delay(50); // Wait for 1000 millisecond(s)
}

void blink_incorrect(){
  for(int i =0; i < 4; i ++){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100); // Wait for 1000 millisecond(s)
    digitalWrite(LED_BUILTIN, LOW);
    delay(100); // Wait for 1000 millisecond(s)
  }
}

void check_button_and_play(){
  
  int pitch = 0;
  for (uint8_t i = 0; i < numTones; i++) {
    if (digitalRead(buttonPins[i]) == LOW && buttonPrev[i] == HIGH) {
      pitch = buttonTones[i];
      if (pitch) {
        tone(SPEAKER_PIN, pitch);
        if(pitch == melody[step]){
          Serial.println("You wouldn't get this from any other guy :)");
          blink_correct();
          step += 1;
        } else {
          Serial.println("You let me down :(");
          blink_incorrect();
          step = 0;
          }
      }
      noTone(SPEAKER_PIN);

    }
    buttonPrev[i] = digitalRead(buttonPins[i]);
  }

  if(step > 14){
    success = true;
  }  
  
}

void print_flag(){

  if(j == 0) { 
    Serial.print("Never gonna give! Never gonna give!\nptctf{");
  }

  if (j == 32){
    j +=1;
    Serial.print('}');
  } 

  if(j == 33) return;

  Serial.print(char(flag[j] ^ mask[j % 26]));
  j += 1;

}
void setup() {
  Serial.begin(115200); 
  Serial.print("wow\n");
  
  for (uint8_t i = 0; i < numTones; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    buttonPrev[i] = digitalRead(buttonPins[i]);
  }
  pinMode(SPEAKER_PIN, OUTPUT);
}

void play() {
  int notelength;
  notelength = beatlength * rhythmn[b];

  digitalWrite(LED_BUILTIN, HIGH);
  delay(10);
  digitalWrite(LED_BUILTIN, LOW);
  if (melody[b] > 0) {
    tone(SPEAKER_PIN, melody[b], notelength);
  }

  b++;
  if (b >= sizeof(melody) / sizeof(int)) {
    success = false;
    finished = true;
  }

  delay(notelength);
  noTone(SPEAKER_PIN);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(10);
  digitalWrite(LED_BUILTIN, LOW); 
  delay(notelength * beatseparationconstant);

}


void loop() {

if (!finished){
  check_button_and_play();
  if (success == true) {
    print_flag();
    play();
  }
}
};


