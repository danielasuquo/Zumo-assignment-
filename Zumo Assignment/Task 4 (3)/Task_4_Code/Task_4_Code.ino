#include <Wire.h>
#include <Zumo32U4.h>

// Change next line to this if you are using the older Zumo 32U4
// with a black and green LCD display:
// Zumo32U4LCD display;
Zumo32U4OLED display;

Zumo32U4Buzzer buzzer;
Zumo32U4Motors motors;
Zumo32U4ButtonA buttonA;
Zumo32U4LineSensors lineSensors;
Zumo32U4IMU imu;

#include "TurnSensor.h"
//L3G gyro;

// the Code will be divided to different modes
// AUTO for Autonomous control of the Zumo
// MANU for Manual control of the Zumo
// The default mode is MANU till the user changes the mode using the GUI
String MODE = "MANU"; 

// This is the maximum speed the motors will be allowed to turn.
// (400 lets the motors go at top speed; decrease to impose a speed limit)
const int MAX_SPEED = 100;
int turnSpeed = 80;
int motorSpeed = 80;

#define NUM_SENSORS 5
uint16_t lineSensorValues[NUM_SENSORS];

bool useEmitters = true;

// Sets up special characters for the display so that we can show
// bar graphs.
void loadCustomCharacters()
{
  static const char levels[] PROGMEM = {
    0, 0, 0, 0, 0, 0, 0, 63, 63, 63, 63, 63, 63, 63
  };
  display.loadCustomCharacter(levels + 0, 0);  // 1 bar
  display.loadCustomCharacter(levels + 1, 1);  // 2 bars
  display.loadCustomCharacter(levels + 2, 2);  // 3 bars
  display.loadCustomCharacter(levels + 3, 3);  // 4 bars
  display.loadCustomCharacter(levels + 4, 4);  // 5 bars
  display.loadCustomCharacter(levels + 5, 5);  // 6 bars
  display.loadCustomCharacter(levels + 6, 6);  // 7 bars
}

void printBar(uint8_t height)
{
  if (height > 8) { height = 8; }
  const char barChars[] = {' ', 0, 1, 2, 3, 4, 5, 6, (char)255};
  display.print(barChars[height]);
}

void calibrateSensors()
{
  display.clear();

  // Wait 1 second and then begin automatic sensor calibration
  // by rotating in place to sweep the sensors over the line
  delay(1000);
  for(uint16_t i = 0; i < 120; i++)
  {
    if (i > 30 && i <= 90)
    {
      motors.setSpeeds(-100, 100);
    }
    else
    {
      motors.setSpeeds(100, -100);
    }

    lineSensors.calibrate();
  }
  motors.setSpeeds(0, 0);
}

// Shows a bar graph of sensor readings on the display.
// Returns after the user presses A.
void showReadings()
{
  display.clear();

  while(!buttonA.getSingleDebouncedPress())
  {
    lineSensors.readCalibrated(lineSensorValues);

    display.gotoXY(0, 0);
    for (uint8_t i = 0; i < NUM_SENSORS; i++)
    {
      uint8_t barHeight = map(lineSensorValues[i], 0, 1000, 0, 8);
      printBar(barHeight);
    }
  }
}

void setup() {
  // Uncomment if necessary to correct motor directions:
  //motors.flipLeftMotor(true);
  //motors.flipRightMotor(true);
  Serial1.begin(9600);
  Serial1.setTimeout(1);

  lineSensors.initFiveSensors();

  loadCustomCharacters();

  // Play a little welcome song
  buzzer.play(">g32>>c32");

  // Wait for the user button to be pressed and released
  display.clear();
  display.print(F("Press A"));
  display.gotoXY(0, 1);
  display.print(F("to calib"));
  buttonA.waitForButton();

  calibrateSensors();

  showReadings();

  turnSensorSetup();
  delay(500);
  turnSensorReset();
  
  // Play music and wait for it to finish before we start driving.
  display.clear();
  display.print(F("Go!"));
  buzzer.play("L16 cdegreg4");
  while(buzzer.isPlaying());
}



// Turn left
void turnLeft(int degrees) {
  turnSensorReset();
  motors.setSpeeds(-turnSpeed, turnSpeed);
  int angle = 0;
  do {
    delay(1);
    turnSensorUpdate();
    angle = (((int32_t)turnAngle >> 16) * 360) >> 16;
  } while (angle < degrees);
  motors.setSpeeds(0, 0);
}

// Turn right
void turnRight(int degrees) {
  turnSensorReset();
  motors.setSpeeds(turnSpeed, -turnSpeed);
  int angle = 0;
  do {
    delay(1);
    turnSensorUpdate();
    angle = (((int32_t)turnAngle >> 16) * 360) >> 16;
  } while (angle > -degrees);
  motors.setSpeeds(0, 0);
}

void loop() {
  turnSensorUpdate();
  int angle = (((int32_t)turnAngle >> 16) * 360) >> 16;
  char x = Read_Serial();
  if(MODE == "MANU")
  {
    Manual(x);
  }else{
    Autonomous(x);
  }
}

char Read_Serial(){
  char x = ' ';
  if (Serial1.available()){
    x = (char) Serial1.read();
    //Serial.println(x);
    // Recieved character
    // if M for switch to Manual Mode
    // if A for switch to Autonomous Mode
    if(x == 'M' || x == 'S'){
      Stop();
      MODE = "MANU";
      Serial1.println("MANU");
    }else if(x == 'A'){
      MODE = "AUTO";
      Serial1.println("AUTO");
    }
  }
  return x;
}

void Manual(char x){
  if (x == 'F'){
    Go_Forward();
  }else if(x == 'B'){
    Go_Backward();
  }else if(x == 'R'){
    Go_Right();
  }else if(x == 'L'){
    Go_Left();
  }else if(x == 'Q'){
    GyroLeft();
  }else if(x == 'E'){
    GyroRight();
  }else if(x == 'S'){
    Stop();
  }
}

void Autonomous(char x){
  // Navigate current line segment until we enter an intersection.
  if(x == 'Q'){
    GyroLeft();
  }else if(x == 'E'){
    GyroRight();
  }else{
  followSegment();
  }
}

void followSegment(){
   // Read the line sensors.
   lineSensors.read(lineSensorValues, useEmitters ? QTR_EMITTERS_ON : QTR_EMITTERS_OFF);

   int thresh = 500;

   if(lineSensorValues[0] >= thresh && lineSensorValues[4] <= thresh){
    Go_Right();
   }else if(lineSensorValues[0] <= thresh && lineSensorValues[4] >= thresh){
    Go_Left();
   }else if(lineSensorValues[0] >= thresh && lineSensorValues[4] >= thresh){
    Stop();
    MODE = "MANU";
    Serial1.println("MANU");
   }else{
    Go_Forward();
   }
}

void Go_Forward(){
  // Direction : Forward
  motors.setLeftSpeed(motorSpeed);
  motors.setRightSpeed(motorSpeed);
  delay(100);
}

void Go_Backward(){
  // Direction : Backward
  motors.setLeftSpeed(-motorSpeed);
  motors.setRightSpeed(-motorSpeed);
  delay(10);
}

void Go_Right(){
  // Direction : Right
  motors.setLeftSpeed(turnSpeed);
  motors.setRightSpeed(-turnSpeed);
  delay(10);
}

void GyroRight(){
  // Direction : Right
  // Turn right 45 degrees using the gyro.
  int angle = (((int32_t)turnAngle >> 16) * 360) >> 16;
  turnRight(90);
}

void Go_Left(){
  // Direction : Left
  motors.setLeftSpeed(-turnSpeed);
  motors.setRightSpeed(turnSpeed);
  delay(10);
}

void GyroLeft(){
  // Direction : Left
  // Turn left 45 degrees using the gyro.
  int angle = (((int32_t)turnAngle >> 16) * 360) >> 16;
  turnLeft(90);
}

void Stop(){
  // Direction : Stop
  motors.setLeftSpeed(0);
  motors.setRightSpeed(0);
}
