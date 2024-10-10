from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.graphics import Color, Rectangle
from collections import deque

# Define a Kivy BoxLayout class to hold our labels and graphs
class SensorBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SensorBoxLayout, self).__init__(orientation='horizontal', **kwargs)

        # Create a vertical layout for the labels with a larger font size
        self.info_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        font_size = '30sp'  # Specify the font size for the labels
        self.spo2_label = Label(text='Oxygen Saturation: 0%', font_size=font_size)
        self.hr_label = Label(text='Heart Rate: 0bpm', font_size=font_size)
        self.temp_label = Label(text='Temperature: 0.00°C', font_size=font_size)
        self.info_layout.add_widget(self.spo2_label)
        self.info_layout.add_widget(self.hr_label)
        self.info_layout.add_widget(self.temp_label)

        # Add the info layout to the main layout
        self.add_widget(self.info_layout)

        # Create a vertical layout for the graphs
        self.graphs_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)

        # Graph for SpO2
        self.spo2_graph = Graph(xlabel='Time', ylabel='SPO2 (%)', xmin=0, xmax=100, ymin=85, ymax=100)
        self.spo2_plot = MeshLinePlot(color=[1, 0, 0, 1])
        self.spo2_graph.add_plot(self.spo2_plot)
        self.graphs_layout.add_widget(self.spo2_graph)

        # Graph for Heart Rate
        self.hr_graph = Graph(xlabel='Time', ylabel='Heart Rate (BPM)', xmin=0, xmax=100, ymin=50, ymax=150)
        self.hr_plot = MeshLinePlot(color=[0, 1, 0, 1])
        self.hr_graph.add_plot(self.hr_plot)
        self.graphs_layout.add_widget(self.hr_graph)

        # Graph for Temperature
        self.temp_graph = Graph(xlabel='Time', ylabel='Temperature (°C)', xmin=0, xmax=100, ymin=35, ymax=40)
        self.temp_plot = MeshLinePlot(color=[0, 0, 1, 1])
        self.temp_graph.add_plot(self.temp_plot)
        self.graphs_layout.add_widget(self.temp_graph)

        # Add the graphs layout to the main layout
        self.add_widget(self.graphs_layout)

        # Deques for storing data
        self.spo2_data = deque(maxlen=100)
        self.hr_data = deque(maxlen=100)
        self.temp_data = deque(maxlen=100)

    def update_graphs(self, itter, spo2, hr, temp):
        # Append new data to the deques
        self.spo2_data.append(spo2)
        self.hr_data.append(hr)
        self.temp_data.append(temp)

        # Update the plots with new data
        self.spo2_plot.points = [(i, self.spo2_data[i]) for i in range(len(self.spo2_data))]
        self.hr_plot.points = [(i, self.hr_data[i]) for i in range(len(self.hr_data))]
        self.temp_plot.points = [(i, self.temp_data[i]) for i in range(len(self.temp_data))]

        # Update the labels
        self.spo2_label.text = f'Oxygen Saturation: {spo2}%'
        self.hr_label.text = f'Heart Rate: {hr}bpm'
        self.temp_label.text = f'Temperature: {temp:.2f}°C'

# Create a Kivy App class that builds the UI
class SensorApp(App):
    def build(self):
        self.layout = SensorBoxLayout()
        # Schedule the read_from_serial function to be called every 4 seconds
        Clock.schedule_interval(self.read_from_serial, 4)
        return self.layout

    def read_from_serial(self, dt):
        # Replace with your actual serial port reading logic
        # Here's an example of data being simulated
        iter_val, spo2, hr, temp = self.simulate_sensor_data()
        self.layout.update_graphs(iter_val, spo2, hr, temp)

    def simulate_sensor_data(self):
        # This function simulates sensor data.
        # Replace this with the actual data reading and parsing logic
        import random
        return (random.randint(1, 100), random.randint(90, 100),
                random.randint(60, 100), random.uniform(36.5, 37.5))
