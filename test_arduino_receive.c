#include <Servo.h>

Servo myServo; // Create a servo object

void setup()
{
    Serial.begin(9600); // Start serial communication at 9600 baud rate
    myServo.attach(9);  // Attach the servo to pin 9
}

void loop()
{
    if (Serial.available() > 0)
    {
        // Read the incoming data (e.g., "45,10" for angle=45, distance=10)
        String data = Serial.readStringUntil('\n');

        // Parse the data into angle and distance
        int commaIndex = data.indexOf(',');                    // Find the comma separator
        int angle = data.substring(0, commaIndex).toInt();     // Extract angle
        int distance = data.substring(commaIndex + 1).toInt(); // Extract distance

        // Control the servo based on the angle
        myServo.write(angle); // Move the servo to the specified angle

        // Optional: Print the received data to the Serial Monitor for debugging
        Serial.print("Angle: ");
        Serial.print(angle);
        Serial.print(", Distance: ");
        Serial.println(distance);
    }
}