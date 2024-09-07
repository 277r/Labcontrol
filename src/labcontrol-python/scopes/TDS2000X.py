import pyvisa as visa
import numpy as np
from labcontrol import Wave
from time import sleep


class TDS2000X():
    _idn = ""
    _inst = None
    
    def capture_wave(self, channel="CH1"):

        """
            copied code below from
             https://github.com/tektronix/Programmatic-Control-Examples/blob/master/Examples/Oscilloscopes/BenchScopes/src/SimplePlotExample/tbs_simple_plot.py
        """
        self._inst.write('data:encdg RIBINARY')
        self._inst.write('wfmpre:byt_nr 1')
        
        # force display wave, if wave is not displayed, CURV? will fail
        self._inst.write(f"SELect:{channel} ON")
        #channel selection, if this value is not defined, scope will not return data and a timeoutError can occur
        self._inst.write(f"DATA:SOURCE {channel}")
        bin_wave = self._inst.query_binary_values('CURVe?', datatype='b', container=np.array)
        print("query ended")
        record = int(self._inst.query('wfmpre:nr_pt?'))
        tscale = float(self._inst.query('wfmpre:xincr?'))
        tstart = float(self._inst.query('wfmpre:xzero?'))
        vscale = float(self._inst.query('wfmpre:ymult?'))  # volts / level
        voff = float(self._inst.query('wfmpre:yzero?'))  # reference voltage
        vpos = float(self._inst.query('wfmpre:yoff?'))  # reference position (level)
        #print(self._inst.query("WFMPre?"))

        # create scaled vectors
        # horizontal (time)
        total_time = tscale * record
        tstop = tstart + total_time
        scaled_time = np.linspace(tstart, tstop, num=record, endpoint=False)
        # vertical (voltage)
        unscaled_wave = np.array(bin_wave, dtype='double') # data type conversion
        scaled_wave = (unscaled_wave - vpos) * vscale + voff
        self._scaledYData = scaled_wave
        # add Yunits so that the user knows what units the scope acquired. user should already know what data is acquired and does not need this, but this will help        
        return Wave(scaled_wave, self._inst.query(f"WFMpre:YUNit?"), scaled_time)
    
    def hold_acquisition(self):
        self._inst.write("ACQuire:STATE STOP")
        
    def continue_acquisition(self):
        self._inst.write("ACQuire:STOPAfter RUNSTOP")
        self._inst.write("ACQuire:STATE RUN")
    
    def single_sequence(self):
        self._inst.write("ACQuire:STATE OFF")
        self._inst.write("ACQuire:MODe SAMple")
        
        self._inst.write("ACQuire:STOPAfter SEQuence")
        
        self._inst.write("ACQuire:STATE on")
        while self._inst.query("ACQuire:STATE?") != "0":
            sleep(1)
        print("acquisition finished")
    
    
    def autoset(self, channel, waveform = "SINGLECYcle"):
        self._inst.write(f"DATA:SOURCE {channel}")
        self._inst.write(f"AUTOSet EXECute")
        self._inst.write(f"AUTOSet:VIEW {waveform}")
        
    def measure(self, channel, type):
        self._inst.write(f"MEASUrement:IMMed:SOUrce[1] {channel}")
        self._inst.write(f"MEASUrement:IMMed:TYPe {type}")
        return self._inst.query("MEASUrement:IMMed:VALue?")
    
    
    def set_vertical_scale(self, channel, scale):
        self._inst.write(f"{channel}:SCAle {scale}")
        
    def set_horizontal_scale(self, scale):
        self._inst.write(f"HORizontal:MAIn:SCAle {scale}")


    
