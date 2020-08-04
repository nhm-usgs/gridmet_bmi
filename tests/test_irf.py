# from io import StringIO

from numpy.testing import assert_almost_equal
# import numpy as np
# import yaml
#
# from six.moves import range
from gridmet_bmi import BmiGridmet


def test_component_name():
    model = BmiGridmet()

    name = model.get_component_name()
    assert name == "Gridmet_BMI"
    assert model.get_component_name() is name


def test_start_time():
    model = BmiGridmet()
    model.initialize()

    assert_almost_equal(model.get_start_time(), 0.0)


def test_end_time():
    model = BmiGridmet()
    model.initialize()

    assert_almost_equal(model.get_end_time(), 1.0)
