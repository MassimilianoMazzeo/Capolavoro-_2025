#include <DHT.h>
 
#define DHTPIN 3        // Pin a cui è collegato il sensore DHT11
#define DHTTYPE DHT11     // Specifica che stai usando un sensore DHT11
 
DHT dht(DHTPIN, DHTTYPE);  // Crea un oggetto DHT per leggere i dati dal sensore

int tempRosso = 8; // temperatura
int tempBlu = 9; // temperatura 
int umRosso = 10; // umidità
int umVerde = 11; // umidità
float sogliaAlta = 25.0; // soglia temperatura
float sogliaBassa = 20.0; 
float umMinore = 30;
float umMaggiore = 80;
 
void setup() {
  pinMode(tempRosso, OUTPUT);
  pinMode(tempBlu, OUTPUT);
  pinMode(umRosso, OUTPUT);
  pinMode(umVerde, OUTPUT);  
  Serial.begin(9600);      // Per monitorare i valori della temperatura
  dht.begin();             // Inizializza il sensore DHT
}
 
void loop() {
  float temp = dht.readTemperature();  // Legge la temperatura dal sensore DHT11
  float um = dht.readHumidity(); //Legge l'umidità
  if (isnan(temp)) {  // Controlla se c'è stato un errore nella lettura
    Serial.println("Errore di lettura dal sensore DHT11!");
    return;
  }
  

  Serial.print(temp);
  Serial.print(", ");
  Serial.println(um);



  // Controlla la temperatura e accende i LED in base ai valori delle soglie
  if (temp >= sogliaAlta) {
    digitalWrite(tempRosso, HIGH);
  } else digitalWrite(tempRosso, LOW);
  
  if (um >= umMaggiore){
     digitalWrite(umRosso, HIGH);
  } else digitalWrite(umRosso, LOW);
  delay(500);  // Ritardo di 2 secondi tra le letture del sensore
}
