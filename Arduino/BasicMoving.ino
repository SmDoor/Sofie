// ---------------------------------------------------------------------------
// Example NewPing library sketch that does a ping about 20 times per second.
// ---------------------------------------------------------------------------

#include <NewPing.h>
#include <queue.h>
#include <string.h>

#define TRIGGER_PIN  1  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     0  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
#define BENBL 9
#define BPHASE 4
#define AENBL 10
#define APHASE 8
#define CONTROLL 12
#define FORWARD 0
#define BACKWARD 1

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup()
{
    randomSeed(micros()/4);
    Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
    pinMode(BENBL, OUTPUT);
    pinMode(BPHASE, OUTPUT);
    pinMode(AENBL, OUTPUT);
    pinMode(APHASE, OUTPUT);
    pinMode(CONTROLL, OUTPUT);
}

void moveStraight(double speed, bool direction)
{
    uint8_t dir = direction ? LOW : HIGH;
    analogWrite(BENBL, 400 * speed);
    digitalWrite(BPHASE, dir);
    analogWrite(AENBL, 400 * speed);
    digitalWrite(APHASE, dir);
}

void turnLeft(double speed, bool direction)
{
    uint8_t dir = direction ? LOW : HIGH;
    analogWrite(BENBL, 400 * speed);
    digitalWrite(BPHASE, dir);
    analogWrite(AENBL, 50 * speed);
    digitalWrite(APHASE, dir);
}

void turnRight(double speed, bool direction)
{
    uint8_t dir = direction ? LOW : HIGH;
    analogWrite(BENBL, 50 * speed);
    digitalWrite(BPHASE, dir);
    analogWrite(AENBL, 400 * speed);
    digitalWrite(APHASE, dir);
}

void brake()
{
    analogWrite(BENBL, 0);
    analogWrite(AENBL, 0);
}

void takePhoto()
{
    String res;
    String res2;
    
    Serial.println("STOPPED");
    delay(20);

    if(Serial.available() > 0) res= Serial.readString();
    if(res=="WAIT")
    {
        while(true)
        {
            if(Serial.available() > 0)
            {
                 String res2 = Serial.readString();
                 if(res2=="GO")
                 {
                    Serial.println("WENT");
                    break;
                 }
            }
        }
    }
}
void testSerial()
{
    while(true)
    {
        Serial.println("STOPPED");
        delay(100);
        String res;
        String res2;
        if(Serial.available() > 0) res= Serial.readString();
        if(res=="WAIT")
        {
            while(true)
            {
                if(Serial.available() > 0)
                {
                     String res2 = Serial.readString();
                     if(res2=="GO")
                     {
                        Serial.println("WENT");
                        break;
                     }
                }
            }
        }
        delay(2000);
    }
}
void loop()
{
    //testSerial();
    queue<int> q;
    digitalWrite(CONTROLL, HIGH);
    delay(30);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
    //Serial.print("Ping: ");
    //Serial.print(sonar.ping_cm()); // Send ping, get distance in cm and print result (0 = outside set distance range)
    //Serial.println("cm");
    
    int dist = 1000;
    bool turning = false;
    int sum = 0;
    bool direction;
    bool waiting=true;

    while (true)
    {
        delay(30);                     // Wait 50ms between pings (about 20 pings/sec). 29ms should be the shortest delay between pings.
        //Serial.print("Ping: ");
        dist = sonar.ping_cm();
        //Serial.println(dist); // Send ping, get distance in cm and print result (0 = outside set distance range)
        //Serial.println("cm");

        //moveStraight(0.2, FORWARD);
        
        if(dist>0 && dist<200) 
        {
            q.push(dist);
            sum += dist;
            //rial.println(dist);
        
        
            if(q.length()>=10) 
            {
                moveStraight(0.2, FORWARD);
                
                int s;
                q.pop(s);
                sum-=s;
                //if(sum < 0) sum = 0;
    
                double idx = sum/10;
                direction = (random(0, 100) % 2 == 0);
                
                if(idx < 10)
                {
                    brake();
                    takePhoto();
                    q.deleteQueue();
                    sum = 0;
                    moveStraight(0.2, BACKWARD);
                    delay(1500);
    
                    if(direction) turnLeft(0.3, FORWARD);
                    else turnRight(0.3, FORWARD);
                    delay(1500);
                    brake();
                }
                /*if(idx < 10) //10
                {
                    brake();
                    moveStraight(0.3, BACKWARD); //0.5
                    delay(1000);
                    
                    if(direction) turnLeft(0.4, FORWARD);//1
                    else turnRight(0.4, FORWARD); //1
                    delay(2000);
                }*/
            }
         }
    }
}
