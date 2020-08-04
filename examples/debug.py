import matplotlib.pyplot as plt
from gridmet_bmi import BmiGridmet
import numpy as np
from pymt.models import PRMSSurface
from pathlib import Path
def print_times(x):
    print(x.get_start_time())
    print(x.get_time_step())
    print(x.get_time_units())
    print(x.get_current_time())
    print(x.get_end_time())

x = BmiGridmet()
x.initialize('gridmet_bmi.yaml')
print_times(x)
x.update()
print_times(x)
tmp = 0