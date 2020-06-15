from pymt.models import PRMSSurface
from pathlib import Path
from gridmet_bmi import Gridmet

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

data = Gridmet("1981-04-07", end_date="1981-04-21", hrumap=True, hru_id=m.get_value('nhm_id'), wght_file=wght)
print(data)