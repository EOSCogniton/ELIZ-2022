#include <FlexCAN.h>
#include <stdlib.h>

//Initialisation des variables

//Variable OSEF
const int ledPin=13;

//Variable VCU
int T_HV = 0; //temp batterie HV
int progressbar_T_HV = 0; //ProgressBar temp batterie HV
int pct_HV = 0;//pct batterie HV
int pct_LV = 0;//pct batterie LV

bool APPS_FAULT;
bool APPS_FAULT_is_active;

bool isPb = 0;

int pb = 0;
String Name_pb ="";
int Pic_pb = 0;
int msglen=4;

//Variables CAN
// static uint8_t hex[17] = "0123456789abcdef"; //Nécessaire pour hexDump

// CAN functions-------------------------------------------------------------
// static void hexDump(uint8_t dumpLen, uint8_t *bytePtr) //Permet d'afficher dans le Serial Menitor le message Hex reçu
// {
//   uint8_t working;
//   while( dumpLen-- ) {
//     working = *bytePtr++;
//     Serial.write( hex[ working>>4 ] );
//     Serial.write( hex[ working&15 ] );
//   }
//   Serial.write('\r');
//   Serial.write('\n');
// }

static String hex2msg(uint8_t dumpLen, uint8_t *bytePtr) //Avoir tous les messages de la tram can
{
  uint8_t working;
  String hextomsg;
  while( dumpLen-- ) {
    working = *bytePtr++;
    hextomsg+=String((working>>4),HEX);
    hextomsg+=String(working&15,HEX) ;
    hextomsg+= " ";
  }
  return hextomsg;
}

static String hex2msgpoint(uint8_t dumpLen, uint8_t *bytePtr, int i) //avoir seulement le ieme message de la tram can
{
  int dumpLenfixed=dumpLen;
  uint8_t working;
  String hextomsg;
  String bellepou;
  while( dumpLen-- ) {
    working = *bytePtr++;
    if(dumpLen!=dumpLenfixed-i-1)
    {
      bellepou+=String((working>>4),HEX);
      bellepou+=String(working&15,HEX) ;
    }
    else{
      hextomsg+=String((working>>4),HEX);
      hextomsg+=String(working&15,HEX) ;
    }
  }
  return hextomsg;
}

static int CharToHex(char str[]) // Obtiens un entier hex depuis un hex en char
{
  return (int) strtol(str, 0, 16);
}

static int StrToHex(String msgstr) //Obtiens un entier hex depuis un hex en string
{
  char* msgchar = const_cast<char*>( msgstr.c_str() );
  return (int) CharToHex(msgchar);
}

// -------------------------------------------------------------
void setup(void)
{
  //Code NSC
  Serial1.begin(9600);
  pinMode(ledPin,OUTPUT);
  delay(100);

  //Code CAN
  delay(1000);
  Serial.println(F("Hello Teensy 3.6 dual CAN Test."));

  Can0.begin(500000);// On lance la communication CAN à 500000 baud

  //if using enable pins on a transceiver they need to be set on
  pinMode(2, OUTPUT);
  pinMode(35, OUTPUT);

  digitalWrite(2, HIGH);
  digitalWrite(35, HIGH);

}


// -------------------------------------------------------------


void loop() {
  // CAN loop
  CAN_message_t inMsg;
  String msgread="";
  int nmsg;

  // Affichage en boucle du msg can
  // while (Can0.available()) 
  // {
  //   Can0.read(inMsg);
  //   // msgread = hex2msg(8, inMsg.buf);
  //   Serial.print(inMsg.id,HEX);
  //   Serial.print('\n');
  //   hexDump(1, inMsg.buf);
  //   // Serial.print("CAN bus 0: "+msgread+'\n');
  //   Serial.println(F("Receiver is alive"));
  // }

  //Affichage de parties du msg
  // String pct_HVstr=msgread[3];
  // pct_HVstr+=msgread[4];
  // Serial.print("String : "+pct_HVstr+"\n");
  // char* pct_HVchar=const_cast<char*>( pct_HVstr.c_str() );
  // Serial.print("Char : ");
  // Serial.print(pct_HVchar);
  // Serial.print("\n");
  // pct_HV=StrToHex(pct_HVchar);
  // Serial.print("value : ");
  // Serial.print(pct_HV);
  // Serial.print("\n");

  // Si on veut de la lumière LOL
  // Serial.println(F("Teensy running !"));
  // digitalWrite(ledPin,HIGH);
  // delay(100);
  // digitalWrite(ledPin,LOW);
  // delay(100);


if(Can0.available()){
  Can0.read(inMsg);
  if(String(inMsg.id,HEX)=="38"){
    Can0.end();
    for (int i=0; i<msglen;i++){
      msgread=hex2msgpoint(msglen,inMsg.buf,i);
      nmsg=StrToHex(msgread);
      Serial.print(nmsg);
      if(i==0){ //Attention, le i correspondant à la variable adéquate doit être vu du côté du code du VCU, au niveau Main/CAN/Dashboard
        pct_LV=nmsg;
      }
      else if(i==1){
        pct_HV=nmsg;
      }
      else if(i==2){
        T_HV=nmsg;
      }
      else{
        APPS_FAULT=nmsg;
        if(APPS_FAULT==0 and APPS_FAULT_is_active==1){
          APPS_FAULT_is_active=0;
        }
      }
    }
    isPb=APPS_FAULT_is_active;
    msgread = hex2msg(msglen, inMsg.buf);
    //Serial.print("CAN bus 0: ID= "+String(inMsg.id,HEX)+" -- Hex= "+msgread+'\n');
    Can0.begin(500000);
  }
}

//Maj des valeurs sur l'écran
  progressbar_T_HV = round(T_HV*(100/60));
  Serial1.print("bat_HV_temp.val=");  // This is sent to the nextion display to set what object name (before the dot) and what atribute (after the dot) are you going to change.
  Serial1.print(progressbar_T_HV); //Change progressbar HV temp
  Serial1.write(0xff);  // We always have to send this three lines after each command sent to the nextion display.
  Serial1.write(0xff);
  Serial1.write(0xff);

  Serial1.print("temp_HV.val=");
  Serial1.print(T_HV); //Change value HV temp
  Serial1.write(0xff);
  Serial1.write(0xff);
  Serial1.write(0xff);

  Serial1.print("bat_HV_pct.val=");
  Serial1.print(pct_HV); //Change progressbar HV lvl percentage
  Serial1.write(0xff);
  Serial1.write(0xff);
  Serial1.write(0xff);

  Serial1.print("pct_HV.val=");  
  Serial1.print(pct_HV); //Change value HV lvl percentage
  Serial1.write(0xff);  
  Serial1.write(0xff);
  Serial1.write(0xff);

  Serial1.print("bat_LV_pct.val=");
  Serial1.print(pct_LV); //Change progressbar LV lvl percentage
  Serial1.write(0xff);
  Serial1.write(0xff);
  Serial1.write(0xff);

  Serial1.print("pct_LV.val=");
  Serial1.print(pct_LV); //Change value LV lvl percentage
  Serial1.write(0xff);
  Serial1.write(0xff);
  Serial1.write(0xff);
  

  if(T_HV<40){//Change color progressbar HV temp
    Serial1.print("bat_HV_temp.pco=1632"); 
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  else if(T_HV>=40 && T_HV<=50){
    Serial1.print("bat_HV_temp.pco=64512");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  else{
    Serial1.print("bat_HV_temp.pco=64512");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  
  if(pct_HV<20){ //Change color progressbar HV lvl percentage
    Serial1.print("bat_HV_pct.pco=63488");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  else if(pct_HV>=20 && pct_HV<=40){
    Serial1.print("bat_HV_pct.pco=64512");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  else{
    Serial1.print("bat_HV_pct.pco=1632");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }


  if(pct_LV<20){ //Change color progressbar LV lvl percentage
    Serial1.print("bat_LV_pct.pco=63488");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  else if(pct_LV>=20 && pct_LV<=40){
    Serial1.print("bat_LV_pct.pco=64512");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }
  else{
    Serial1.print("bat_LV_pct.pco=1632");  // This is sent to the nextion display to set what object name (before the dot) and what atribute (after the dot) are you going to change.
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  }

  //Changement de page en cas de probleme
  if(APPS_FAULT==1){ //Traitement APPS FAULT
    if(APPS_FAULT_is_active==0){
      Serial1.print("issue.t1.txt=");
      Serial1.print("\"APPS Fault\"");
      Serial1.write(0xff);
      Serial1.write(0xff);
      Serial1.write(0xff);

      Serial1.print("issue.p1.pic=");
      Serial1.print(7);
      Serial1.write(0xff);
      Serial1.write(0xff);
      Serial1.write(0xff);

      Serial1.print("sys2=");
      Serial1.print(1);
      Serial1.write(0xff);
      Serial1.write(0xff);
      Serial1.write(0xff);

      APPS_FAULT_is_active=1;
      isPb=APPS_FAULT_is_active;
    }
    
  }
  if(isPb==0){
    Serial1.print("sys2=");
    Serial1.print(0);
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);
  
    Serial1.print("p1.aph=0");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);

    Serial1.print("t1.aph=0");
    Serial1.write(0xff);
    Serial1.write(0xff);
    Serial1.write(0xff);

  }
}
