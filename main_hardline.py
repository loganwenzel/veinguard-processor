import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

def live_plot(ax_ir, ax_red, data_ir, data_red, line_ir, line_red, ir_value, red_value, window_size=5):
    data_ir.append(ir_value)
    data_red.append(red_value)

    smoothed_ir = np.convolve(data_ir, np.ones(window_size)/window_size, mode='valid')
    smoothed_red = np.convolve(data_red, np.ones(window_size)/window_size, mode='valid')

    # Adjust lengths to match
    diff_ir = len(data_ir) - len(smoothed_ir)
    diff_red = len(data_red) - len(smoothed_red)

    line_ir.set_ydata([None]*diff_ir + list(smoothed_ir))
    line_red.set_ydata([None]*diff_red + list(smoothed_red))

    ax_ir.relim()
    ax_ir.autoscale_view()
    ax_red.relim()
    ax_red.autoscale_view()

    line_ir.set_color('blue')  # Set color for IR line (e.g., blue)
    line_red.set_color('red')  # Set color for red line

    plt.pause(0.1)

plt.ion()  # Enable interactive mode

serial_port = '/dev/cu.usbserial-130'  # Change this to your actual serial port
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)

max_data_points = 100
data_sensor1_ir = deque([0] * max_data_points, maxlen=max_data_points)
data_sensor1_red = deque([0] * max_data_points, maxlen=max_data_points)
data_sensor2_ir = deque([0] * max_data_points, maxlen=max_data_points)
data_sensor2_red = deque([0] * max_data_points, maxlen=max_data_points)

fig, (ax1_ir, ax1_red, ax2_ir, ax2_red) = plt.subplots(4, 1, sharex=True)
x_domain = range(0, max_data_points)
line_sensor1_ir, = ax1_ir.plot(x_domain, data_sensor1_ir, label='Sensor 1 IR')
line_sensor1_red, = ax1_red.plot(x_domain, data_sensor1_red, label='Sensor 1 Red')
line_sensor2_ir, = ax2_ir.plot(x_domain, data_sensor2_ir, label='Sensor 2 IR')
line_sensor2_red, = ax2_red.plot(x_domain, data_sensor2_red, label='Sensor 2 Red')

ax1_ir.set_title('Sensor 1 IR Data')
ax1_red.set_title('Sensor 1 Red Data')
ax2_ir.set_title('Sensor 2 IR Data')
ax2_red.set_title('Sensor 2 Red Data')

ax1_ir.set_ylabel('IR Values')
ax1_red.set_ylabel('Red Values')
ax2_ir.set_ylabel('IR Values')
ax2_red.set_ylabel('Red Values')

ax2_red.set_xlabel('Time (samples)')

ax1_ir.legend()
ax1_red.legend()
ax2_ir.legend()
ax2_red.legend()

plt.tight_layout()

plt.show()  # Display the plot initially

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        values = line.split(',')
        ir_value_sensor1 = int(values[0])
        red_value_sensor1 = int(values[1])
        ir_value_sensor2 = int(values[2])
        red_value_sensor2 = int(values[3])

        live_plot(ax1_ir, ax1_red, data_sensor1_ir, data_sensor1_red, line_sensor1_ir, line_sensor1_red, ir_value_sensor1, red_value_sensor1)
        live_plot(ax2_ir, ax2_red, data_sensor2_ir, data_sensor2_red, line_sensor2_ir, line_sensor2_red, ir_value_sensor2, red_value_sensor2)

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")
