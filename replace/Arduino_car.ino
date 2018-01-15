#include <Wire.h>

#define SLAVE_ADDRESS 0x04
typedef enum {STOP,FORWARD,BACKWARD,RIGHT,LEFT}Action;
Action cmd=STOP; 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(13,OUTPUT);
  Wire.begin(SLAVE_ADDRESS);

  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.println("Ready!");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (cmd==STOP){
    analogWrite(5, 0); // 右輪反轉
    analogWrite(6, 0);// 右輪正轉
    digitalWrite(7,LOW);
    digitalWrite(8, LOW);
    analogWrite(9, 0);// 左輪正轉
    analogWrite(10,0);// 左輪反轉
  }
  else if (cmd==FORWARD){
    digitalWrite(7,HIGH);
    digitalWrite(8, HIGH);
    analogWrite(5, 0); // 右輪反轉
    analogWrite(6, 150);// 右輪正轉
    analogWrite(9, 95);// 左輪正轉
    analogWrite(10,0);// 左輪反轉
    delay(800);
    digitalWrite(7,LOW);
    digitalWrite(8, LOW);
    cmd=STOP;
  }
  else if (cmd==BACKWARD){
    digitalWrite(7,HIGH);
    digitalWrite(8, HIGH);
    analogWrite(5, 150); // 右輪反轉
    analogWrite(6, 0);// 右輪正轉
    analogWrite(9, 0);// 左輪正轉
    analogWrite(10,135);// 左輪反轉
    delay(800);
    digitalWrite(7,LOW);
    digitalWrite(8, LOW);
    cmd=STOP;
  }
  else if (cmd==RIGHT){
    digitalWrite(7,HIGH);
    digitalWrite(8, HIGH); 
    analogWrite(5, 150); // 右輪反轉
    analogWrite(6, 0);// 右輪正轉
    analogWrite(9, 150);// 左輪正轉
    analogWrite(10,0);// 左輪反轉
    delay(150);
    digitalWrite(7,LOW);
    digitalWrite(8, LOW);
    cmd=STOP;
  }
  else if (cmd==LEFT){
    digitalWrite(7,HIGH);
    digitalWrite(8, HIGH);
    analogWrite(5, 0); // 右輪反轉
    analogWrite(6, 150);// 右輪正轉 
    analogWrite(9, 0);// 左輪正轉
    analogWrite(10,150);// 左輪反轉
    delay(150);
    digitalWrite(7,LOW);
    digitalWrite(8, LOW);
    cmd=STOP;
  }
} 

void receiveData(int byteCount){
  while(Wire.available()){
    int number = Wire.read();
    if(number!=255)
      cmd=(Action)number;
    else
      cmd=STOP;
    Serial.print("data received: ");
    Serial.println(cmd);
  }
}

void sendData(int ACK){
  Wire.write(ACK);
}
