import matplotlib.pyplot as plt
from gridmet_bmi import Gridmet
import numpy as np
from pymt.models import PRMSSurface
from pathlib import Path

wght = '../../onhm-fetcher-parser/Data/weights.csv'
run_dir = '../../bmi-test-projects/prms/pipestem'
config_file = 'control.default'
print(Path(run_dir).exists())
print((Path(run_dir) / config_file).exists())

m = PRMSSurface()
print(m.name)
m.name

m.initialize(config_file, run_dir)
m.get_value('nowtime')
m.get_value('nhm_id')

data = Gridmet("1981-04-07", end_date="1981-04-21", map=True, hru_id=m.get_value('nhm_id'), wght_file=wght)
# data = Gridmet("2019-03-14", end_date="2019-03-24")

ds = data.tmax.data[:,:]
tmp = 0
m.finalize()