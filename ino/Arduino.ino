int i;
const int pot = A0;
const int btns[2] = {A1,A2};
enum ctrl{Next,Reset};
String lectura;

void setup() {
  // put your setup code here, to run once:
  for(i=0; i<2; i++){
    pinMode(btns[i],INPUT);
  }
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  lectura = "";

  lectura += String(analogRead(pot))+" ";
  lectura += String(!digitalRead(btns[Next])) + " ";
  lectura += String(!digitalRead(btns[Reset])) ;

  Serial.println(lectura);
  delay(200);
}
