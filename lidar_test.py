import PyLidar2
import time # Time module
port = "/dev/ttyUSB0" #linux
Obj = PyLidar2.YdLidarX4(port) #PyLidar2.your_version_of_lidar(port,chunk_size) 
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 30: #scan for 30 seconds
        print(gen.next())
        time.sleep(0.5)
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")
