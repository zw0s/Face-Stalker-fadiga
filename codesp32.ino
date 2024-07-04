#include <Wire.h>
#include <ESP32Servo.h>

// Criação dos objetos para cada servo
Servo ServoX;
Servo ServoY;

float prevX = 95;			// Valor inicial do ServoX
float prevY = 45;			// Valor inicial do ServoY
float fatorIncremento = 1;	//	Incremento para movimentação dos servos

// Pinos ligados aos servos
const int servoX=4; 		
const int servoY=2; 


int command = 0;		// Variável que determina o sentido de movimentação
int menorLX = 40;       //Valor inicial que representa o menor valor que o ESP32 pode enviar ao servo
int maiorLX = 135;      //Valor inicial que representa o maior valor que o ESP32 pode enviar ao servo

int menorLY = 8;        //Valor inicial que representa o menor valor que o ESP32 pode enviar ao servo
int maiorLY = 82;      	//Valor inicial que representa o maior valor que o ESP32 pode enviar ao servo


// Função executado ao receber algum dado do Master(Raspberry)
void receiveEvent(int howMany) {
  while (Wire.available()) {
    int command = Wire.read();  
   
    if (command == 2 && prevX > menorLX){
      prevX = prevX - fatorIncremento;			// Esquerda
    }
    else if (command == 1 && prevX < maiorLX){
      prevX= prevX + fatorIncremento;			// Direita
    }
    else if (command == 3 && prevY > menorLY){
      prevY = prevY - fatorIncremento;			// Baixo
    }
    else if (command == 4 && prevY < maiorLY){
      prevY = prevY + fatorIncremento;			// Cima
    }
    else {
      Serial.println(command);
    }
	
	//Envia valores aos servos
    ServoX.write(prevX);
    ServoY.write(prevY);
    delay(2);
  }
}
 
void setup() {
  // Configura na comunicação I2C o ESP32 como Slave como endereço 0x8
  Wire.begin(0x8);
  
  // Atribuição dos objetos ás portas lógicas
  ServoX.attach(servoX);
  ServoY.attach(servoY);

  // Coloca os servos na posição inicial
  ServoX.write(prevX);
  ServoY.write(prevY);
  
  // Determina qual a função deve ser chamada ao receber algum dado               
  Wire.onReceive(receiveEvent);  
} 

void loop() {
delay(2);
}