double calcLightIntensity( int AnVal, int Resistor) {
  double Vout = AnVal*0.0048828125;
  int lux = ((2500/Vout-500)/Resistor);
  return lux;
  
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int analogVal = analogRead(A0);
  int Resistance = 10;

  Serial.print("light intensity");
  Serial.print(int(calcLightIntensity(analogVal, Resistance)));
  delay(1000);

}
