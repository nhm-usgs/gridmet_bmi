from ._version import get_versions
from .bmi import BmiOnhm
from .onhm import Onhm
from .helpers import np_get_wval, getaverage

__all__ = ["BmiOnhm", "Onhm"]

__version__ = get_versions()["version"]
del get_versions
