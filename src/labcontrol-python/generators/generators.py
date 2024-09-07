
from generators.SDG1000 import SDG1000
import pyvisa as visa

class Generator():
    _idn = ""
    _inst = None
    #Generator is just a wrapper for all existing generators. innerGenerator contains all the functionalities based for that specific generator
    innerGenerator = None
    
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
                print("error occured")
                
            if name==None:    
                if self._idn.find("SDG,SDG10") > -1:
                        self._inst = dev
                        print("Found tektronix sdg1000 generator")
                        print(f"IDN: {self._idn}")
                        print(f"URL: {dev}")
                        self.innerGenerator = SDG1000
                        break
            else:
                if self._idn.find(name) > -1:
                        self._inst = dev
                        print(f"Found generator: {self._idn}\n pattern used: {name}")
                        # set innerScope to right value, but how to know which class to use?
                        self.innerGenerator = SDG1000
                        break
                
        return
    
    
    # generic for all devices, should only be used when you know what you're doing
    def query(self, inst=""):
        return self.innerGenerator._inst.query(self,inst)
    def write(self, inst=""):
        return self.innerGenerator._inst.write(self,inst)
    
    
    def set_wave_type(self, channel="CH1", wavetype="SINE"):
        return self.innerGenerator.set_wave_type(self, channel, wavetype)
        
    def set_frequency(self, channel="CH1", freq=1000):
        return self.innerGenerator.set_frequency(self, channel, freq)
    
    def set_amplitude(self, channel="CH1", amp=1):
        return self.innerGenerator.set_amplitude(self, channel, amp)
    def set_offset(self, channel="CH1", offset=0):
        return self.innerGenerator.set_offset(self, channel, offset)

    def enable_output(self, channel="CH1"):
        return self.innerGenerator.enable_output(self, channel)
        
    def disable_output(self, channel="CH1"):
        return self.innerGenerator.disable_output(self, channel)

    # to add: duty, phase, symmetry settings. 
    # make sure that wavetype patterns in user code are translated to wavetypes in scopes using translation table
    # query value state to make sure that values to set have been received by the device 
    # to add when nothing better to do: wave modulation