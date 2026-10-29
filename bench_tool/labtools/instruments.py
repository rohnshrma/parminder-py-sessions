# labtools/instruments.py - a module inside the labtools PACKAGE
# (a package = a folder containing __init__.py; the empty __init__.py marks it as importable)
# usage from bench_tool/main.py:  from labtools.instruments import PowerMeter

class PowerMeter:                  # blueprint (class) for a power meter device
    def __init__(self,port):       # constructor: runs automatically when PowerMeter(...) is created
        self.port = port           # store the port on the object (e.g. "COM3")

    def connect(self):             # method: self gives access to this object's data
        print(f"connected to {self.port}")

    def disconnect(self):
        print(f"disconnected from {self.port}")
