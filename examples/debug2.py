import matplotlib.pyplot as plt
from gridmet_bmi import BmiGridmet, Gridmet
import numpy as np

gridmet = Gridmet(lazy=True)
assert len(getattr(gridmet, 'tmax')) == 1
print(len(gridmet.tmax))
tmp = 0