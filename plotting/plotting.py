import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def live_plotter(time_index, s1_IR, s1_Red, lines=[], pause_time=0.01):
    if len(lines) < 8:  # We have 6 lines and 2 axes now
        plt.ion()

        # Create a 1x2 grid of subplots
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20,6))

        # Plot Sensor 1 data on the first subplot
        line1, = ax1.plot(time_index, s1_IR, '-', alpha=0.8, label="S1 - IR", color='orange')
        line2, = ax1.plot(time_index, s1_Red, '-', alpha=0.8, label="S1 - Red", color='red')
        ax1.set_ylabel('Light Reflection (Lumins)', fontweight='bold')
        ax1.set_xlabel('Time (0.1s)', fontweight='bold')
        ax1.set_title('Sensor 1 Real-time Data', fontweight='bold')
        ax1.legend()

        # Plot Sensor 2 data on the second subplot
        # line4, = ax2.plot(time_index, s2_IR, '-', alpha=0.8, label="S2 - IR", color='orange')
        # line5, = ax2.plot(time_index, s2_Red, '-', alpha=0.8, label="S2 - Red", color='red')
        # ax2.set_ylabel('Light Reflection (Lumins)', fontweight='bold')
        # ax2.set_xlabel('Time (0.1s)', fontweight='bold')
        # ax2.set_title('Sensor 2 Real-time Data', fontweight='bold')
        # ax2.legend()

        # Reset the lines list and add the lines and axes
        # lines[:] = [line1, line2, ax1, line4, line5, ax2]
        lines[:] = [line1, line2, ax1]
    else:
        # Update the data for all lines
        lines[0].set_data(time_index, s1_IR)
        lines[1].set_data(time_index, s1_Red)
        # lines[4].set_data(time_index, s2_IR)
        # lines[5].set_data(time_index, s2_Red)

        # Adjust x-axis for both subplots
        lines[3].set_xlim(min(time_index), max(time_index))
        lines[7].set_xlim(min(time_index), max(time_index))

        # Dynamically adjust y-axis for both subplots
        lines[3].set_ylim(min(min(s1_IR), min(s1_Red)) - 5, max(max(s1_IR), max(s1_Red)) + 5)
        # lines[7].set_ylim(min(min(s2_IR), min(s2_Red)) - 5, max(max(s2_IR), max(s2_Red)) + 5)

        plt.pause(pause_time)
