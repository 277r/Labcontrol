
channel_table={
    "CH1" : "C1",
    "CH2" : "C2"
}

class SDG1000():
    _idn = ""
    _inst = None
    

    def set_wave_type(self, channel, wavetype):
        self._inst.write(f"{channel_table.get(channel)}:BSWV WVTP,{wavetype}")
        return 
        
    def set_frequency(self, channel, freq):
        self._inst.write(f"{channel_table.get(channel)}:BSWV FRQ,{freq}")
        return
    
    def set_amplitude(self, channel, amp):
        self._inst.write(f"{channel_table.get(channel)}:BSWV AMP,{amp}")
        return
    def set_offset(self, channel, offset):
        self._inst.write(f"{channel_table.get(channel)}:BSWV OFST,{offset}")
        return
    
    def enable_output(self, channel="CH1"):
        self._inst.write(f"{channel_table.get(channel)}:OUTP ON")
        return
    
    def disable_output(self, channel):
        self._inst.write(f"{channel_table.get(channel)}:OUTP OFF")
        return     
    
    
    
    
