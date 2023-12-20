

// Set up all Variables
int potA = A0;
int potB = A1;
int potC = A2;
int potD = A3;
bool mute = false;
bool isMuted = false;


// Setup Serial and Input pin
void setup() {
  
  Serial.begin(57600);
  pinMode(2, INPUT);

}


// Main loop
void loop() {
  
  // Send potA data through serial
  
  // Sends prefix "a" to later determine what this value changes
  Serial.print("a");
  // Sends a 2 demimal float value from 0 to 1
  Serial.print(String(float(map(analogRead(potA), 0, 1023, 0, 1000))/1000));
  // Ends the line 
  Serial.print("\n");
  
  
  // Send potB data through serial

  // Sends prefix "b" to later determine what this value changes
  Serial.print("b");
  // Sends a 2 demimal float value from 0 to 1
  Serial.print(String(float(map(analogRead(potB), 0, 1023, 0, 1000))/1000));
  // Ends the line 
  Serial.print("\n"); 

  
  // Send potC data through serial

  // Sends prefix "c" to later determine what this value changes
  Serial.print("c");
  // Sends a 2 demimal float value from 0 to 1
  Serial.print(String(float(map(analogRead(potC), 0, 1023, 0, 1000))/1000));
  // Ends the line 
  Serial.print("\n"); 

  // Send potD data through serial

  // Sends prefix "d" to later determine what this value changes
  Serial.print("d");
  // Sends a 2 demimal float value from 0 to 1
  Serial.print(String(float(map(analogRead(potD), 0, 1023, 0, 1000))/1000));
  // Ends the line 
  Serial.print("\n");   
  
  // Handles the mutting by the push button
  while (digitalRead(2) == HIGH)
  {
      // Sends a value with prefix "e" to determine when to mute the speakers
      if (isMuted == false)
      {
        mute = !mute;
    
        Serial.print("e");
        Serial.print(mute);
        Serial.print("\n");

      }
      isMuted = true;
      
 }
  
  isMuted = false;
  
  delay(5);


}
