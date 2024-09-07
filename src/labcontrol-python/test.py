# generic libraries to aid timing and plotting graphs
from time import *
import matplotlib.pyplot as plt

# le'abcontrol
import labcontrol as lc


supply = lc.Supply()

meter = lc.Multimeter()

print(meter.measure_voltage("DC"))
