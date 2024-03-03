/*
 * 
 * Test Software 
 * Valencia - 2020 
 * 
 * SENSOR - OMRON E2A-...-M12 C1 M2, NPN, NO (Normally Open) 
 * The cables of the sensor there are three cables which are that 
 * BROWN ==> 12V to 24V (Power supply of the sensor)
 * BLACK ==> output of the sensor 
 * BLUE ==> GND ground
 * 
 * ELECTROMAGNET 
 * Power Supply 24V
 * The commands of the electromagnet.
 * The commands are 1 and 2. The duty of the command;
 * 
 * 1 ==> ON  Electromagnet is ON  
 * 2 ==> OFF Electromanget is OFF
 * 
 * CONNECTION TO ARDUINO
 * Sensor ==> PIN 7
 * Electromagnet ==> PIN 4
 * Circuit GND ==> GND ARDUINO
 * 
 * !!!!IMPORTANTE!!!! 
 * DONT FORGET THE CONNECT CIRCUIT'S GND TO ARDUINO'S GND
 * IF YOU FORGET IT, THE CHIP OF ARDUINO CAN NOT WORK
 * 
 */
unsigned long magnetStartMicros;  
unsigned long magnetTimeMicros = 5000;
unsigned long sensorStartMicros;
unsigned long sensorTimeMicros = 500;

// The pinses for connecting to Arduino
int sensor = 8;  // The black cable of the Sensor ==> Arduino PIN 9 
int magnet = 4; // The output of the magnet ==> Arduino PIN 5
bool NewRead, Read; // "calculation()" (LOOK DOWN) funcion uses these values. The sensor reads "Read" ==> first read, "newRead" ==> second read
float NewTime; // "calculation()" funcion (LOOK DOWN) uses these time values

void setup() {
 Serial.begin(9600); 
 Serial.println("Test Starting"); // Save the datas to the Microsoft Excel, this line Clear all what the excel file has in it.
 pinMode(sensor, INPUT); // Configuration's pin of the sensor
 pinMode(magnet, OUTPUT); // Configuration's pin of the electromagnet pinMode(led, OUTPUT);
 NewRead = 0; 
 NewTime = 0;
 }
void loop() {
/* The first if starts to work with micros() funcion. There are 1,000 microseconds in a millisecond and 1,000,000 microseconds in a second. 
 * Then The Arduino's pin waits the command which are 1 and 2.
 * 1 - Electromagnet ON
 * 2 - Electromagnet OFF
 */
  if(micros() - magnetStartMicros >= magnetTimeMicros){
     if (Serial.available()){
      long state = Serial.parseInt(); // Reading the command in the Serial Port
      if(state == 1){
          digitalWrite(magnet, HIGH);
          Serial.println("Electroiman is ON");
          }
        if(state == 2){
          digitalWrite(magnet, LOW);
          Serial.println("Electroiman is OFF");
        }
     }
    magnetStartMicros += magnetTimeMicros; // Do it again the same thing when the command send it
   }
/*
 * The second-if in the loop works the same logic as the first-if
 * The different thing is that when the sensor reads, send signal to Arduino's pin and
 * calculation() funcion calculate the datas which the sensor has already read. Everthing 
 * will be appared in the Serial Monitor. It is located on the right of the screen.
 */
  if (micros() -  sensorStartMicros >= sensorTimeMicros) { // sensor
    
    calculation();
   
    sensorStartMicros += sensorTimeMicros; // do it again later
  }   
}
void calculation(){
  
  Read = NewRead;
  NewRead = digitalRead(sensor);
 
  if(not Read && NewRead){
     NewTime = micros();

     Serial.println(NewTime);   
  }
  
}
