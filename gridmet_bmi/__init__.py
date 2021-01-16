from ._version import get_versions
from .bmi_gridmet import BmiGridmet

# from examples.bmi import BmiGridmet
from .gridmet import Gridmet
from .helpers import getaverage, np_get_wval

__all__ = ["BmiGridmet", "Gridmet", "np_get_wval", "getaverage"]

__version__ = get_versions()["version"]
del get_versions
