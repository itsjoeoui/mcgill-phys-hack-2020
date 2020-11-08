const int rightTriggerPin = 5; // Trigger Pin of Ultrasonic Sensor
const int rightEchoPin = 6; // Echo Pin of Ultrasonic Sensor
const int frontTriggerPin = 2; // Trigger Pin of Ultrasonic Sensor
const int frontEchoPin = 3; // Echo Pin of Ultrasonic Sensor
const int rotationDelay = 2750; // time it takes to rotate 90 degrees at max speed
int dir = 1;
int length;
int width;
int cycle = 0;

#include <Servo.h>

Servo leftservo;  
Servo rightservo;  

double measure_temp() {
    int sensorInput = analogRead(A0);
    double temp = (double)sensorInput / 1024;       
    //multiply by 5V to get voltage
    temp = temp * 5;   
    temp = temp - 0.5;    //Subtract the offset 
    temp = temp * 100;    //Convert to degrees 
    return temp;
}

double measure_distance_front() {
     //Front ULTRASONIC 
    //create a variable to save the duration in
    int distance;
    long frontDuration;  
    //clear the ping pin
    digitalWrite(frontTriggerPin, LOW);
    delayMicroseconds(2);
    //send the 10 microsecond trigger
    digitalWrite(frontTriggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(frontTriggerPin, LOW);
    //get the pulse duration in microseconds
    frontDuration = pulseIn(frontEchoPin, HIGH);
    distance = int(frontDuration*0.034/2);
    delay(10);
    return distance;
}

double measure_distance_right() {
    
    //RIGHT ULTRASONIC 
    //create a variable to save the duration in
    int distance;
    long rightDuration;  
    //clear the ping pin
    digitalWrite(rightTriggerPin, LOW);
    delayMicroseconds(2);
    //send the 10 microsecond trigger
    digitalWrite(rightTriggerPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(rightTriggerPin, LOW);
    //get the pulse duration in microseconds
    rightDuration = pulseIn(rightEchoPin, HIGH);
    distance = int(rightDuration*0.034/2);
    delay(10);
    return distance;
}


void rotate(bool l) {
    
    if (l) {
        rightservo.write(100);
        leftservo.write(100);
        delay(4218);
    } else {
        rightservo.write(80);
        leftservo.write(80);
        delay(4218);
    }
    rightservo.write(90);
    leftservo.write(90);

}


bool calibrate(double p) {
    double c = measure_distance_right();
    int diff = int(c - p);
    if (diff > 0) {
        rightservo.write(180-diff*20);

    }
    else if (diff < 0) {
        leftservo.write(-diff*20);

    }

    delay(200);
    rightservo.write(180);
    leftservo.write(0);
    if (abs(diff) < 2)
        return true; 
}

void stop() {
    rightservo.write(90);
    leftservo.write(90);
}

void move_forward() {
    rightservo.write(180);
    leftservo.write(0);
}


void setup() {
    //set up the Serial
    Serial.begin(9600);

    //setup the pin modes  
    pinMode(rightTriggerPin, OUTPUT);
    pinMode(rightEchoPin, INPUT);

    pinMode(frontTriggerPin, OUTPUT);
    pinMode(frontEchoPin, INPUT);
    
    leftservo.attach(9);  
    rightservo.attach(10);

    rightservo.write(90);
    leftservo.write(90);

    //determine dimensions of plate
    //we get the ultra sensor readings, then we rotate 180 degrees and get readings again. 
    //We sum these reading to get the total length and width of the plate
    double y1 = measure_distance_front();
    double x1 = measure_distance_right();
    rotate(true);
    delay(500);
    rotate(true);


    double y2 = measure_distance_front();
    double x2 = measure_distance_right();
    delay(500);

    length = int(y1 + y2);
  
    width = int(x1 + x2);
   
    //setup at corner
    move_forward();
    while (true) {
        int dist = measure_distance_front();
        if (dist < 15) {
            stop();
            break;
        }
        double p = measure_distance_right();
        delay(500);
        bool trash = calibrate(p);
        delay(70);
    }
    rotate(true);


    move_forward();
    while (true) {
        int dist = measure_distance_front();
        if (dist < 15) {
            stop();
            break;
        }
        double p = measure_distance_right();
        delay(500);
        bool trash = calibrate(p);
        delay(70);
    }
    delay(500);
    rotate(true);
    delay(500);

}

void loop() {
    
    int distancetoStop = cycle*14 + 15;
    move_forward();
    double p = measure_distance_right();
    delay(500);
    bool pass = calibrate(p);
    if (pass) {
        delay(20);
        int test = measure_distance_front();
        if (test > distancetoStop) {
            if (dir == 1) {
                int yPos = length - int(measure_distance_front());
                int xPos = int(measure_distance_right());
                Serial.print(xPos);
                Serial.print(",");
                Serial.print(yPos);
                Serial.print(",");
                Serial.print(measure_temp());
            }
            else if (dir == 2) {
                int xPos = width- int(measure_distance_front());
                int yPos = length - int(measure_distance_right());
                Serial.print(xPos);
                Serial.print(",");
                Serial.print(yPos);
                Serial.print(",");
                Serial.print(measure_temp());
            }
            else if (dir == 3) {
                int yPos = int(measure_distance_front());
                int xPos = width - int(measure_distance_right());
                Serial.print(xPos);
                Serial.print(",");
                Serial.print(yPos);
                Serial.print(",");
                Serial.print(measure_temp());
            }
            else if (dir == 4) {
                int xPos = int(measure_distance_front());
                int yPos = int(measure_distance_right());
                Serial.print(xPos);
                Serial.print(",");
                Serial.print(yPos);
                Serial.print(",");
                Serial.print(measure_temp());
            }
            Serial.println(" ");
        } else {
            dir++;
            if (dir == 4) {
                cycle++;
            }
            if (dir == 5) {
                dir = 1;
            }
            rotate(true);
            
        }
        
    }
    

}
