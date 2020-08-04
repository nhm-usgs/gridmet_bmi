import matplotlib.pyplot as plt
from gridmet_bmi import BmiGridmet, Gridmet
import numpy as np

gridmet = Gridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True)
assert len(getattr(gridmet, 'tmax')) == 1
tmp = 0