# for SPD, channels are CH<x>
# for SDG, channels are C<x>
# makes no sense to me

class SPD3303XE:
    _idn = "" 
    _inst = None
    
    def enable_output(self, channel="CH1"):
        self._inst.write(f"OUTP {channel},ON")
    def disable_output(self, channel="CH1"):
        self._inst.write(f"OUTP {channel},OFF")
        
    def set_voltage(self, voltage: float, channel="CH1"):
        self._inst.write(f"{channel}:VOLT {voltage:.3f}")
    
    def set_current(self, current: float, channel="CH1"):
        self._inst.write(f"{channel}:CURR {current:.3f}")
    
    def get_voltage(self, channel="CH1"):
        return self._inst.query(f"{channel}:VOLT?")

    def get_current(self, channel="CH1"):
        return self._inst.query(f"{channel}:CURR?")
    
    def measure_voltage(self, channel="CH1"):
        return self._inst.query(f"MEAS:VOLT? {channel}")
    
    def measure_current(self, channel="CH1"):
        return self._inst.query(f"MEAS:CURR? {channel}")

    def measure_power(self, channel="CH1"):
        return self._inst.query(f"MEAS:POWE? {channel}")
