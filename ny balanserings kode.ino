#include <AccelStepper.h>
#include <MPU6050.h>
#include <Wire.h>

//stepper driver pins
#define PUL_PIN 7
#define DIR_PIN 3
#define ENA_PIN 8

MPU6050 imu;

float angle = 0;
float angleNOW = 0;
float gyroChange = 0;
float offset = 0;
float a = 0.90; // for komplementary filter 90% gyroscope, 10% accelerometer

float X1 = 25.0;
float X2 = 0.9;

AccelStepper stepper(AccelStepper::DRIVER, PUL_PIN, DIR_PIN);


const unsigned long IMU_PERIOD_US = 4000; // 250 hz
unsigned long lastImuTime = 0;
const unsigned long SERIAL_PERIOD_MS = 50; // 20 hz
unsigned long lastSerialTime = 0;


void setup() {
  Serial.begin(115200);

  pinMode(ENA_PIN, OUTPUT);
  digitalWrite(ENA_PIN, LOW);

  stepper.setEnablePin(ENA_PIN);
  stepper.setPinsInverted(false, false, true);
  stepper.enableOutputs();

  stepper.setMaxSpeed(7000);
  stepper.setAcceleration(6000);

  Wire.begin();

  imu.initialize();

  // calibrating imu sensor
  Serial.println("Kalibrerer gyroskop...");
  long sum = 0;
  int samples = 500;
  for (int i = 0; i < samples; i++) {
    int16_t ax, ay, az, gx, gy, gz;
    imu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    sum += gy;
    delay(2);
  }
  offset = sum / (float)samples;
  Serial.print("Offset: ");
  Serial.println(offset);
}

void loop() {
  stepper.runSpeed();

  unsigned long now = micros();

  // imu update loop 
  if (now - lastImuTime >= IMU_PERIOD_US) {
    lastImuTime += IMU_PERIOD_US;

    int16_t accX, accY, accZ, gyroX, gyroY, gyroZ;
    imu.getMotion6(&accX, &accY, &accZ, &gyroX, &gyroY, &gyroZ);

    float dt = IMU_PERIOD_US / 1000000.0;

    //tilt angle from accelerometer
    angleNOW = atan2((float)accY, (float)accZ) * 180.0 / PI;

    //convert gyroscope to degrees pr second
    gyroChange = (gyroY - offset) / 131.0;
    
    // Complementary filter for angle estimation
    angle = a * (angle + gyroChange * dt) + (1 - a) * angleNOW;
    
    //PD Controller
    int pwm = -constrain(X1 * angle + X2 * gyroChange, -300, 300);
    
    // Map control signal to stepper speed
    long speed = map(pwm, -300, 300, -7000, 7000);

    stepper.setSpeed(speed);
  }

// Periodic serial output for debugging
  if (millis() - lastSerialTime >= SERIAL_PERIOD_MS) {
    lastSerialTime = millis();
    Serial.print("angleNOW: ");
    Serial.print(angleNOW);
    Serial.print(" | angle: ");
    Serial.print(angle);
    Serial.print(" | gyro: ");
    Serial.print(gyroChange);
    Serial.print(" | pwm: ");
    Serial.print(-constrain(X1 * angle + X2 * gyroChange, -300, 300));
    Serial.print(" | speed: ");
    Serial.println(stepper.speed());
  }
}
