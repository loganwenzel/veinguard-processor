import serial
import time


def read_from_bluetooth(com_port):
    # Set up the serial connection
    ser = serial.Serial(com_port, 9600)  # replace 9600 with your baud rate
    ser.flushInput()

    try:
        while True:
            # Read a line of data from the serial port
            ser_bytes = ser.readline().decode("utf-8").strip()

            # Print the received data to the console
            print(f"Received: {ser_bytes}")

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        print("Disconnected")

    finally:
        # Ensure the serial connection is closed
        ser.close()


if __name__ == "__main__":
    com_port = "COM9"
    read_from_bluetooth(com_port)
