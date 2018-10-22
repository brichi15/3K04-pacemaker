class LRL:
    def __init__(self,value):
        self.name = "Lower Rate Limit"
        self.parvalue = value
        self.parrange = []
        self.units = ""

class URL:
    def __init__(self,value,prange,units):
        self.name = "Upper Rate Limit"
        self.parvalue = 0
        self.parrange = []
        self.units = ""

class MSR:
    def __init__(self,value,prange,units):
        self.name = "Maximum Sensor Rate"
        self.parvalue = 0
        self.parrange = []
        self.units = ""


            : ,
            "Fixed AV Delay": ,
            "Dynamic AV Delay": ,
            "Sensed AV Delay Offset": ,
            "Atrial Amplitude": , 
            "Ventricular Amplitude": ,
            "Atrial Pulse Width": ,
            "Ventricular Pulse Width": , 
            "Atrial Sensitivity": ,
            "Ventricular Sensitivity": ,
            "VRP": ,
            "ARP": , 
            "PVARP": , 
            "PVARP Extension": ,
            "Hysteresis": ,
            "Rate Smoothing": ,  
            "ATR Duration": ,
            "ATR Fallback Mode": ,
            "ATR Fallback Time": ,
            "Activity Threshold": ,
            "Reaction Time": ,
            "Response Factor": ,
            "Recovery Time": ,
            }
