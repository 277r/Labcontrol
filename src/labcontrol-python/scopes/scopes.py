
from scopes.TDS2000X import TDS2000X
from labcontrol import Wave
import pyvisa as visa
import numpy as np

class Scope():
    _idn = ""
    _inst = None
    #Scope is just a wrapper for all existing scopes. innerScope contains all the functionalities based for that specific scope
    innerScope = None
    
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
                print("error occured trying to get scope identification")
                
            if name == None:
                if self._idn.find("TEKTRONIX,TDS 200") > -1:
                        self._inst = dev
                        print("Found tektronix TDS200XX scope")
                        print(f"IDN: {self._idn}")
                        print(f"URL: {dev}")
                        self.innerScope = TDS2000X
                        break
            else: 
                if self._idn.find(name) > -1:
                    self._inst = dev
                    print(f"Found scope: {self._idn}\n pattern used: {name}")
                    # set innerScope to right value, but how to know which class to use? 
                    # add translation table where specific scope names (TDS2004C) get translated into less specific scope classes (TDS2000X)
                    self.innerScope = TDS2000X
                    break
                
        return
    
    
    # generic for all devices, should only be used when you know what you're doing
    def query(self, inst=""):
        return self.innerScope._inst.query(inst)
    def write(self, inst=""):
        return self.innerScope._inst.write(inst)
    
    def capture_wave(self, channel="CH1", ):
        return self.innerScope.capture_wave(self, channel)
    
    def hold_acquisition(self):
        self.innerScope.hold_acquisition(self)
        
    def continue_acquisition(self):
        self.innerScope.continue_acquisition(self)
        
    def single_sequence(self):
        self.innerScope.single_sequence(self)
    # supported waveforms: SINGLECYCLE, MULTICYCLE, FFT
    def autoset(self, channel="CH1", waveform = "SINGLECYcle"):
        self.innerScope.autoset(self, channel, waveform)
    
    # supported types: CRMS, FREQUENCY, PERIOD, MEAN, PK2PK, MAXIMUM, MINIMUM
    def measure(self, channel="CH1", type="PK2pk"):
        return self.innerScope.measure(self,channel,type)
    
    def set_vertical_scale(self, channel="CH1", scale="1"):
        return self.innerScope.set_vertical_scale(self,channel,scale)
        
    def set_horizontal_scale(self, scale="1"):
        return self.innerScope.set_horizontal_scale(self,scale)
    
    # todo: add trigger source, trigger level, add tektronix SDS compatibility
    # maybe: make sure that device is in set state, when setting a value like range, get the value and check if it's right
    
    
