#include <FlexCAN.h>
#include <stdlib.h>

//Initialisation des variables

//Variable OSEF
const int ledPin=13;

//Variable VCU
int T_HV = 45; //temp batterie HV
int progressbar_T_HV = 50; //ProgressBar temp batterie HV
int pct_HV = 50;//pct batterie HV
int pct_LV = 50;//pct batterie LV
int spd = 0;//vitesse
int spd_meter = 0;//affichage vitesse sur cadran

bool APPS_FAULT = 0;

bool DISP_BTN = 0;
int PAGE=1;
int nPAGE=2;
bool DISP_BTN_not_active = 1;

bool APPS_FAULT_not_active = 1;

bool T_HV_high_not_active = 1;

bool lvl_HV_low_not_active = 1;

bool lvl_LV_low_not_active = 1;

bool noPb = 1;

int msglen=5; //longueur message can +1

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

// static String hex2msg(uint8_t dumpLen, uint8_t *bytePtr) //Avoir tous les messages de la tram can
// {
//   uint8_t working;
//   String hextomsg;
//   while( dumpLen-- ) {
//     working = *bytePtr++;
//     hextomsg+=String((working>>4),HEX);
//     hextomsg+=String(working&15,HEX) ;
//     hextomsg+= " ";
//   }
//   return hextomsg;
// }

static String hex2msgpoint(uint8_t dumpLen, uint8_t *bytePtr, int i)//avoir seulement le ieme message de la tram can
{
  int dumpLenfixed=dumpLen;
  uint8_t working;
  String hextomsg;
  String bellepou;
  while( dumpLen-- ){
    working = *bytePtr++;
    if(dumpLen!=dumpLenfixed-i-1)
    {
      bellepou+=String((working>>4),HEX);
      bellepou+=String(working&15,HEX);
    }
    else{
      hextomsg+=String((working>>4),HEX);
      hextomsg+=String(working&15,HEX);
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

static void SendToScreenData(String instruction,int value)
{
  Serial1.print(instruction);
  Serial1.print(value);
  Serial1.write(0xff); // We always have to send this three lines after each command sent to the nextion display.
  Serial1.write(0xff);
  Serial1.write(0xff);
}

static void SendToScreen(String instruction)
{
  Serial1.print(instruction);
  Serial1.write(0xff); // We always have to send this three lines after each command sent to the nextion display.
  Serial1.write(0xff);
  Serial1.write(0xff);
}

static void ShowIssue(String Issuename, int Picnum)
{ 
  SendToScreen("issue.t1.txt=\""+Issuename+"\"");

  SendToScreenData("issue.p1.pic=",Picnum);

  SendToScreen("page issue");
}

// -------------------------------------------------------------
void setup(void)
{
  //Code NSC
  Serial1.begin(9600);
  pinMode(ledPin,OUTPUT);
  delay(1000);

  //Code CAN
  delay(1000);
  Serial.println(F("Bienvenue dans la console de la Teensy du Dashboard"));

  //if using enable pins on a transceiver they need to be set on
  pinMode(2, OUTPUT);
  pinMode(35, OUTPUT);

  digitalWrite(2, HIGH);
  digitalWrite(35, HIGH);

  Can0.begin(500000);// On lance la communication CAN à 500000 baud
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

// Mise à jour des valeurs si Message Can disponible
  if(Can0.available()){
    Can0.read(inMsg);
    Serial.print("APPS_FAULT=");
    Serial.print(APPS_FAULT);
    Serial.print("\n APPS_FAULT_not_active=");
    Serial.print(APPS_FAULT_not_active);
    Serial.print("\n");
    if(String(inMsg.id,HEX)=="38"){
      Can0.end();
      for (int i=0; i<msglen;i++){
        msgread=hex2msgpoint(msglen,inMsg.buf,i);
        nmsg=StrToHex(msgread);
        Serial.print(nmsg);
        Serial.print("\n");
        if(i==0){ //Attention, le i correspondant à la variable adéquate doit être vu du côté du code du VCU, au niveau Main/CAN/Dashboard
          pct_LV=nmsg;
        }
        else if(i==1){
          pct_HV=nmsg;
        }
        else if(i==2){
          T_HV=nmsg;
        }
        else if(i==3){
          APPS_FAULT=nmsg;
          if(APPS_FAULT==0 and APPS_FAULT_not_active==0){
            SendToScreen("listissues.pic_APPS.aph=0");
            SendToScreen("listissues.text_APPS.aph=0");
            APPS_FAULT_not_active=1;
          }
        }
        else{
          DISP_BTN=nmsg;
          if(DISP_BTN==0 and DISP_BTN_not_active==0){
            DISP_BTN_not_active=1;
          }
          else if(DISP_BTN==1 and DISP_BTN_not_active==1){
            if(PAGE==nPAGE){
              PAGE=1;
            }
            else{
              PAGE++;
            }
            SendToScreenData("page=",PAGE);
          }
        }
      }
      //msgread = hex2msg(msglen, inMsg.buf);
      //Serial.print("CAN bus 0: ID= "+String(inMsg.id,HEX)+" -- Hex= "+msgread+'\n');
      Can0.begin(500000);
    }
  }

//Maj des valeurs sur l'écran
  progressbar_T_HV = round(T_HV*(100/60));//Change progressbar HV temp
  SendToScreenData("bat_HV_temp.val=",progressbar_T_HV);// This is sent to the nextion display to set what object name (before the dot) and what atribute (after the dot) are you going to change.

  SendToScreenData("temp_HV.val=",T_HV);//Change value HV temp

  SendToScreenData("bat_HV_pct.val=",pct_HV);//Change progressbar HV lvl percentage

  SendToScreenData("pct_HV.val=",pct_HV);//Change value HV lvl percentage

  SendToScreenData("bat_LV_pct.val=",pct_LV);//Change progressbar LV lvl percentage
  
  SendToScreenData("pct_LV.val=",pct_LV);//Change value LV lvl percentage
  

  if(T_HV<40){//Change color progressbar HV temp
    SendToScreen("bat_HV_temp.pco=1632");

    if(T_HV_high_not_active==0){
      SendToScreen("listissues.pic_HV_temp.aph=0");
      SendToScreen("listissues.text_HV_temp.aph=0");
      T_HV_high_not_active=1;
    }
  }
  else if(T_HV>=40 && T_HV<=50){
    SendToScreen("bat_HV_temp.pco=64512");
  }
  else{
    SendToScreen("bat_HV_temp.pco=63488");

    if(T_HV_high_not_active==1){
      ShowIssue("Temp Batterie HV > 50°C",2);
      SendToScreen("listissues.pic_HV_temp.aph=127");
      SendToScreen("listissues.text_HV_temp.aph=127");
      T_HV_high_not_active=0;
    }
  }
  

  if(pct_HV<20){ //Change color progressbar HV lvl percentage
    SendToScreen("bat_HV_pct.pco=63488");

    if(lvl_HV_low_not_active==1){
      ShowIssue("Batterie HV < 20 %",9);
      SendToScreen("listissues.pic_HV.aph=127");
      SendToScreen("listissues.text_HV.aph=127");
      lvl_HV_low_not_active=0;
    }
  }
  else if(pct_HV>=20 && pct_HV<=40){
    SendToScreen("bat_HV_pct.pco=64512");
  }
  else{
    SendToScreen("bat_HV_pct.pco=1632");
  }


  if(pct_LV<20){ //Change color progressbar LV lvl percentage
    SendToScreen("bat_LV_pct.pco=63488");

    if(lvl_LV_low_not_active==1){
      ShowIssue("Batterie LV < 20 %",9);
      SendToScreen("listissues.pic_LV.aph=127");
      SendToScreen("listissues.text_LV.aph=127");
      lvl_LV_low_not_active=0;
    }

  }
  else if(pct_LV>=20 && pct_LV<=40){
    SendToScreen("bat_LV_pct.pco=64512");
  }
  else{
    SendToScreen("bat_LV_pct.pco=1632");
  }


//Changement de page en cas de probleme
  if(APPS_FAULT==1){ //Traitement APPS FAULT
    if(APPS_FAULT_not_active==1){
      ShowIssue("APPS Fault", 7);
      SendToScreen("listissues.pic_APPS.aph=127");
      SendToScreen("listissues.text_APPS.aph=127");
      APPS_FAULT_not_active=0;
  
      SendToScreen("main.p1.aph=127");
      SendToScreen("speed.p1.aph=127");

      SendToScreen("main.t1.aph=127");
      SendToScreen("speed.t1.aph=127");
    }
  }
  noPb=APPS_FAULT_not_active && T_HV_high_not_active && lvl_HV_low_not_active && lvl_LV_low_not_active;
}
