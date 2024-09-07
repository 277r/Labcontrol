class SDM3045X:
    _idn = ""
    _inst = None
    def measure_voltage(self, type, range):
        return self._inst.query(f"MEAS:VOLT:{type}? {range}")
    
    def measure_current(self, type, range):
        return self._inst.query(f"MEAS:CURR:{type}? {range}")
    
    

    def measure_capacitance(self, range):
        return self._inst.query(f"MEAS:CAP? {range}")

    def measure_resistanceTW(self, range):
        return self._inst.query(f"MEAS:RES? {range}")

    def measure_resistanceFW(self, range):
        return self._inst.query(f"MEAS:FRES? {range}")
    
    

    def measure_frequency(self):
        return self._inst.query(f"MEAS:FREQ?")

    def measure_period(self):
        return self._inst.query(f"MEAS:PER?")

    def measure_diode_Vf(self):
        return self._inst.query(f"MEAS:DIOD?")
