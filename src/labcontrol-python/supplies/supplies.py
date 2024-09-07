from supplies.SPD3303XE import SPD3303XE
import pyvisa as visa
import numpy as np

class Supply:
    _idn = ""
    _inst = None
    #Supply is just a wrapper for all existing supplies. innerSupply contains all the functionalities based for that specific supply
    innerSupply = None
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
                print(self._idn)
            except:
                print("error occured trying to get supply identification")
                
            if name == None:
                if self._idn.find("Siglent Technologies,SPD3303X-E") > -1:
                        self._inst = dev
                        print("Found Siglent SPD3303X-E supply")
                        print(f"IDN: {self._idn}")
                        print(f"URL: {dev}")
                        self.innerSupply = SPD3303XE
                        break
            else: 
                if self._idn.find(name) > -1:
                    self._inst = dev
                    print(f"Found supply: {self._idn}\n pattern used: {name}")
                    # set innersupply to right value, but how to know which class to use? 
                    # add translation table where specific supply names (TDS2004C) get translated into less specific supply classes (TDS2000X)
                    self.innerSupply = SPD3303XE
                    break
                
        return
    # generic for all devices, should only be used when you know what you're doing
    def query(self, inst=""):
        return self.innerSupply._inst.query(inst)
    def write(self, inst=""):
        return self.innerSupply._inst.write(inst)
    
    def enable_output(self, channel="CH1"):
        return self.innerSupply.enable_output(self, channel)
    def disable_output(self, channel="CH1"):
        return self.innerSupply.disable_output(self, channel)
    def set_voltage(self, voltage: float, channel="CH1"):
        return self.innerSupply.set_voltage(self, voltage, channel)
    def set_current(self, current: float, channel="CH1"):
        return self.innerSupply.set_current(self, current, channel)
    def get_voltage(self, channel="CH1"):
        return self.innerSupply.get_voltage(self, channel)
    def get_current(self, channel="CH1"):
        return self.innerSupply.get_current(self, channel)
    def measure_voltage(self, channel="CH1"):
        return self.innerSupply.measure_voltage(self, channel)
    def measure_current(self, channel="CH1"):
        return self.innerSupply.measure_current(self, channel)
    def measure_power(self, channel="CH1"):
        return self.innerSupply.measure_power(self, channel)

#todo: add timer capabilities, add channel serialization/parallelization options 