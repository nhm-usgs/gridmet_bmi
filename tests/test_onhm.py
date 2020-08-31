import pytest

from gridmet_bmi import Gridmet
from datetime import datetime, timedelta


@pytest.mark.parametrize("var", ("tmax",
                                 "tmin",
                                 "prcp"))
def test_get_var(tmpdir, var):
    with tmpdir.as_cwd():
        gridmet = Gridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True)
        assert len(getattr(gridmet, var)) == 1


def test_end_date_start_date():
    with pytest.raises(ValueError):
        Gridmet(start_date="2019-03-14", end_date="2019-03-13", lazy=True)


def test_end_date_in_the_future():
    future = datetime.now() + timedelta(10)
    with pytest.raises(ValueError):
        Gridmet(start_date="2019-03-14", end_date=future.strftime("%Y-%m-%d"), lazy=True)


def test_bad_date_format():
    with pytest.raises(ValueError):
        Gridmet(start_date="2019/03/14", lazy=True)


@pytest.mark.parametrize("cache_dir", (".", "./cache"))
def test_cache_dir(tmpdir, cache_dir):
    with tmpdir.as_cwd():
        print(cache_dir)
        gridmet = Gridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True, cache_dir=cache_dir)
        print(gridmet.cache_dir)
        assert gridmet.cache_dir.is_absolute()
        assert list(gridmet.cache_dir.glob("*.nc")) == []


def test_cached_data(tmpdir):
    with tmpdir.as_cwd():
        Gridmet(start_date="2010-05-22", end_date="2010-05-22", lazy=False, cache_dir=tmpdir)
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 3


def test_lazy_load(tmpdir):
    with tmpdir.as_cwd():
        gridmet = Gridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True, cache_dir=".")
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 0
        gridmet.tmax
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 1


def test_eager_load(tmpdir):
    with tmpdir.as_cwd():
        Gridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=False, cache_dir=".")
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 3
