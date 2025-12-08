#include <Wire.h>
#include <MPU6050.h>

MPU6050 imu;

float angle = 0;
float angleNOW = 0;
float gyroChange = 0;
float offset = 0;    
float a = 0.98; // for complementary filter 98% gyroscope and 2% accelerometer      
unsigned long timeLast;

// PID parameters
float X1 = 25.0;
float X2 = 0.9;


int MotorENA = 5;     
int MotorIN1 = 2;
int MotorIN2 = 10;

void setup() {

  Serial.begin(9600);
  Wire.begin();
  imu.initialize();

  Serial.println("kalibrering");
  delay(2000);

  long sum = 0;
  int samples = 200;
  //calibration of imu sensor
  for (int i = 0; i < samples; i++) {
    int16_t accX, accY, accZ, gyroX, gyroY, gyroZ;
    imu.getMotion6(&accX, &accY, &accZ, &gyroX, &gyroY, &gyroZ);
    sum += gyroX;
    delay(5);
  }
  offset = sum / (float)samples;

  Serial.print("GyroX offset = ");
  Serial.println(offset);

  pinMode(MotorENA, OUTPUT);
  pinMode(MotorIN1, OUTPUT);
  pinMode(MotorIN2, OUTPUT);

  timeLast = millis();
}

//function to determine speed and direction
void setMotorSpeed(int speed) {

  //mapping the value of the speed between +-255 for the motor
  speed = constrain(speed, -255, 255);

  if (speed >= 0) {
    // Motor fremover
    digitalWrite(MotorIN1, HIGH);
    digitalWrite(MotorIN2, LOW);
    analogWrite(MotorENA, speed);
  } else {
    // Motor bakover
    digitalWrite(MotorIN1, LOW);
    digitalWrite(MotorIN2, HIGH);
    analogWrite(MotorENA, -speed); // positiv PWM
  }
}


void loop() {

  int16_t accX, accY, accZ, gyroX, gyroY, gyroZ;
  imu.getMotion6(&accX, &accY, &accZ, &gyroX, &gyroY, &gyroZ);

  float dt = (millis() - timeLast) / 1000.0;
  timeLast = millis();

  //calculating the current angle
  angleNOW = atan2((float)accY, (float)accZ) * 180.0 / PI;

  // how fast the motor is falling  
  gyroChange = ((float)gyroX - offset) / 131.0;   

  //complementary filter, combines the gyroscope and accelerometer
  angle = a * (angle + gyroChange * dt) + (1 - a) * angleNOW;

  //pid algorithm
  int pwm = -constrain(X1 * angle + X2 * gyroChange, -255, 255);  

  setMotorSpeed(pwm);

  // Debug
  Serial.print("Angle: ");
  Serial.print(angle);
  Serial.print(" | gyro: ");
  Serial.print(gyroChange);
  Serial.print(" | PWM: ");
  Serial.println(pwm);
}
