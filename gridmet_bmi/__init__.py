from ._version import get_versions
from .bmi import BmiGridmet
from .gridmet import Gridmet
from .helpers import np_get_wval, getaverage
from .bmi_gridmet import BmiGridmet

__all__ = ["BmiGridmet", "Gridmet", "np_get_wval", "getaverage", "BmiGridmet"]

__version__ = get_versions()["version"]
del get_versions