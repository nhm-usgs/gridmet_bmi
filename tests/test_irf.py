from io import StringIO

from numpy.testing import assert_almost_equal, assert_array_less
import numpy as np
import yaml

from six.moves import range
from gridmet_bmi import BmiGridmet

def test_component_name():
    model = BmiGridmet("gridmet_bmi_test.yaml")

    name = model.get_component_name()
    assert name == "Gridmet_BMI"
    assert model.get_component_name() is name

def test_start_time():
    model = BmiGridmet("gridmet_bmi_test.yaml")
    model.initialize()

    assert_almost_equal(model.get_start_time(), 0.0)

def test_end_time():
    model = BmiHeat()
    model.initialize()

    assert_almost_equal(model.get_end_time(), 7.0)


