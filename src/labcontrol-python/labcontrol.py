class Wave:
    def __init__(self, arg1, arg2, arg3):
        self.y = arg1
        self.unitY = arg2
        self.time = arg3
        
    y = []
    unitY = ""
    time = []
    
from scopes.scopes import Scope
from generators.generators import Generator
from supplies.supplies import Supply
from multimeters.multimeters import Multimeter