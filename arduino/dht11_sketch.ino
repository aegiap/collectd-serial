#include <dht.h>

#define dht_dpin A0

dht DHT;

void setup(){
  Serial.begin(9600);
   //Let system settle
  delay(4000);
}

void loop(){
  DHT.read11(dht_dpin);

  Serial.print("Current humidity (%) = ");
  Serial.print(DHT.humidity);
  Serial.print(" temperature (C) = ");
  Serial.print(DHT.temperature);
  Serial.print("\n");
  //Don't try to access too frequently...
  delay(1000); 
}

