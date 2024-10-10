import serial
import time
from plotting.plotting import live_plotter
from collections import deque
import threading
from kivy.clock import mainthread

from classes import SensorApp

def read_from_bluetooth(com_port):
    # Set up the serial connection

    ser = serial.Serial()
    ser.port = com_port
    ser.baudrate = 9600  # replace 9600 with your baud rate
    
    if ser.is_open:
        ser.close()

    ser.open()
    ser.flushInput()

    # Initialize plotting
    size = 100
    sensors_itter = deque(maxlen=size)

    s1_spo2_vec = deque(maxlen=size)
    s1_hr_vec = deque(maxlen=size)
    s1_temp_vec = deque(maxlen=size)

    for i in range(size):
        sensors_itter.append(i)
        s1_spo2_vec.append(0)
        s1_hr_vec.append(0) 
        s1_temp_vec.append(0) 
        
    try:
        while True:
            # Read a line of data from the serial port
            ser_bytes = ser.readline().decode("utf-8").strip()
            try:
                # seperating the string by comma, turning it into a float
                s1, s1_IR, s1_Red, s2_IR, s2_Red = map(float, ser_bytes.split(','))

                # live_plotter(x_vec, s1_IR_d, s1_Red_d, s2_IR_d, s2_Red_d)
                #live_plotter(itter, s1_IR_d, s1_Red_d)

            except ValueError:
                print("Invalid input format. Expected format: (second, sensor_1_val, sensor_2_val)")
                continue

            # Print the received data to the console
            print(ser_bytes)

    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        print("\nBluetooth Disconnected...\n")

    finally:
        # Ensure the serial connection is closed
        ser.close()

@mainthread
def update_gui(itter, s1_spo2, s1_hr, s1_temp):
    app = SensorApp.get_running_app()  # Use SensorApp here
    if app:
        app.layout.update_labels(itter, s1_spo2, s1_hr, s1_temp)


if __name__ == "__main__":
    com_port = "/dev/ttys003"

    # Start the Bluetooth reading in a separate thread
    bt_thread = threading.Thread(target=read_from_bluetooth, args=(com_port,), daemon=True)
    bt_thread.start()

    # Start the Kivy application
    #SensorApp().run()