


int pot1 = A0;
int pot2 = A1;
int pot3 = A2;
int pot4 = A3;
bool mute = false;
bool isMuted = false;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(57600);
  pinMode(2, INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  
  Serial.print("a");
  Serial.print(String(float(map(analogRead(pot1), 0, 1023, 0, 1000))/1000));
  Serial.print("\n");
  
  Serial.print("b");
  Serial.print(String(float(map(analogRead(pot2), 0, 1023, 0, 1000))/1000));
  Serial.print("\n"); 

  Serial.print("c");
  Serial.print(String(float(map(analogRead(pot3), 0, 1023, 0, 1000))/1000));
  Serial.print("\n"); 

  Serial.print("d");
  Serial.print(String(float(map(analogRead(pot4), 0, 1023, 0, 1000))/1000));
  Serial.print("\n");   
  
  while (digitalRead(2) == HIGH)
  {
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
