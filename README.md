# veinguard-processor
University of Waterloo Biomedical Engineering 4th year capstone project. Members are Lagan Bansal, Ayden Cauchi, Jesica Chelva, and Logan Wenzel. 

<h2> Setup </h2>
- Ensure arduino code is uploaded and running <br>
- Run ble-scan and ensure BT05 is visible <br>
- ble-serial -d {UUID from ble-scan} to begin connection <br>
- Get the com port value (eg. '/dev/ttys005') by running 'ble-serial -d <UUID>' and set it as com_port = ""
- Enter main.py into terminal
