import serial

def read_from_bluetooth(com_port):
    ser = serial.Serial(com_port, 9600, timeout=1)
    print(f"Connected to {ser.portstr}")

    try:
        while True:
            ser_bytes = ser.readline().decode("utf-8").rstrip()
            if ser_bytes:
                print(ser_bytes)
            else:
                print("No data received. Is the device sending data?")

    except KeyboardInterrupt:
        print("\nBluetooth Disconnected...\n")
    finally:
        ser.close()

if __name__ == "__main__":
    com_port = "/dev/ttys003"  # This should match the virtual serial port
    read_from_bluetooth(com_port)