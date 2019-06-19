
void setup() {
  // put your setup code here, to run once:
  Serial.begin(57600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.write("Hi   | ");
  delay(1);
  //Serial.print("State : ");
 // Serial.print(Serial.available());  Serial.print("    " );
 if(Serial.available())
 {
  Serial.print("Read :   " );  Serial.println(Serial.readStringUntil("\0"));
 }
 
}
