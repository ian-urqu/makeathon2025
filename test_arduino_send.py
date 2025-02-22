import serial
import time

# Set up the serial connection (adjust the port and baud rate as needed)
arduino = serial.Serial(port="COM6", baudrate=9600, timeout=1)
time.sleep(2)  # Wait for the Arduino to initialize


def send_data_to_arduino(angle, distance):
    # Format the data as "angle,distance" (e.g., "45,10")
    data = f"{angle},{distance}\n"
    arduino.write(data.encode())  # Send the data to Arduino
    print(f"Sent: {data.strip()}")  # Print the sent data for debugging


# Example: Send angle and distance data to the Arduino
angle = 45  # Example angle (in degrees)
distance = 10  # Example distance (in arbitrary units)
send_data_to_arduino(angle, distance)

# Close the serial connection
arduino.close()
