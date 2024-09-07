from multimeters.SDM3045X import SDM3045X
import pyvisa as visa
import numpy as np

class Multimeter:
    _idn = ""
    _inst = None
    #Multimeter is just a wrapper for all existing multimeters. innerMeter contains all the functionalities based for that specific Multimeter
    innerMeter = None
    
    def __init__(self, name=None):
        rm = visa.ResourceManager()
        
        devices = rm.list_resources()
         
        for url in devices:
            dev = rm.open_resource(url)
            dev.timeout = 10000  # ms
            #dev.encoding = 'latin_1'
            dev.read_termination = '\n'
            dev.write_termination = '\n'
            # add error handling, make sure devices are fully reset from error state before querying
            try:
                self._idn = dev.query("*idn?")
            except:
                print("error occured trying to measure multimeter identification")
                
            if name == None:
                if self._idn.find("Siglent Technologies,SDM3045X") > -1:
                        self._inst = dev
                        print("Found Siglent SDM3045X multimeter")
                        print(f"IDN: {self._idn}")
                        print(f"URL: {dev}")
                        self.innerMeter = SDM3045X
                        break
            else: 
                if self._idn.find(name) > -1:
                    self._inst = dev
                    print(f"Found multimeter: {self._idn}\n pattern used: {name}")
                    # set innerMeter to right value, but how to know which class to use? 
                    # add translation table where specific meter names (TDS2004C) measure translated into less specific scope classes (TDS2000X)
                    self.innerMeter = SDM3045X
                    break
                
        return
    # generic for all devices, should only be used when you know what you're doing
    def query(self, inst=""):
        return self.innerMeter._inst.query(inst)
    def write(self, inst=""):
        return self.innerMeter._inst.write(inst)
    
    def measure_voltage(self, type, range="AUTO"):
        return self.innerMeter.measure_voltage(self, type, range) 
    
    def measure_current(self, type, range="AUTO"):
        return self.innerMeter.measure_current(self, type, range) 
    
    

    def measure_capacitance(self, range="AUTO"):
        return self.innerMeter.measure_capacitance(self, range) 

    def measure_resistanceTW(self, range="AUTO"):
        return self.innerMeter.measure_resistanceTW(self, range) 

    def measure_resistanceFW(self, range="AUTO"):
        return self.innerMeter.measure_resistanceFW(self, type, range) 
    
    

    def measure_frequency(self):
        return self.innerMeter.measure_frequency(self, type) 

    def measure_period(self):
        return self.innerMeter.measure_period(self, type) 

    def measure_diode_Vf(self):   
        return self.innerMeter.measure_diode_Vf(self, type) 
    
    #todo: add continuity, add temperature measurement