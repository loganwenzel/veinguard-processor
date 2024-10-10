import serial
import time
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

# Define the serial port and baud rate
serial_port = '/dev/cu.usbserial-120'  # Change this to your actual serial port
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)

def is_outlier(value, data, threshold=1000):
    """
    Check if the value is an outlier based on a simple threshold.
    """
    if not data:
        return False

    # Calculate the difference between the value and the median of the data
    diff = abs(value - np.median(data))

    # If the difference is greater than the threshold, consider it an outlier
    return diff > threshold

max_data_points = 100
initial_value = 1000  # Change this to an appropriate initial value
data_sensor1 = deque([initial_value] * max_data_points, maxlen=max_data_points)
data_sensor2 = deque([initial_value] * max_data_points, maxlen=max_data_points)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
x_domain = range(0, max_data_points)
line_sensor1, = ax1.plot(x_domain, data_sensor1, label='Sensor 1')
line_sensor2, = ax2.plot(x_domain, data_sensor2, label='Sensor 2')

ax1.set_title('Sensor 1 Data')
ax2.set_title('Sensor 2 Data')
ax1.set_ylabel('IR Values')
ax2.set_ylabel('IR Values')
ax2.set_xlabel('Time (samples)')

ax1.legend()
ax2.legend()

plt.tight_layout()
plt.ion()  # Enable interactive mode

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        values = line.split(',')
        ir_value_sensor1 = int(values[0])
        ir_value_sensor2 = int(values[1])

        # Check for outliers
        if is_outlier(ir_value_sensor1, data_sensor1) or is_outlier(ir_value_sensor2, data_sensor2):
            # Skip updating the plot if an outlier is detected
            continue

        data_sensor1.append(ir_value_sensor1)
        line_sensor1.set_ydata(data_sensor1)

        data_sensor2.append(ir_value_sensor2)
        line_sensor2.set_ydata(data_sensor2)

        ax1.relim()
        ax1.autoscale_view()

        ax2.relim()
        ax2.autoscale_view()

        plt.draw()
        plt.pause(0.1)

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")
