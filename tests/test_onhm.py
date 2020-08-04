import pytest

from gridmet_bmi import BmiGridmet


@pytest.mark.parametrize("var", ("daily_maximum_temperature",
                                 "daily_minimum_temperature",
                                 "precipitation_amount"))
def test_get_var(tmpdir, var):
    with tmpdir.as_cwd():
        gridmet = BmiGridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True)
        assert len(getattr(gridmet, var)) == 1


def test_end_date_start_date():
    with pytest.raises(ValueError):
        BmiGridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True)


def test_end_date_in_the_future():
    with pytest.raises(ValueError):
        BmiGridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True)


def test_bad_date_format():
    with pytest.raises(ValueError):
        BmiGridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True)


@pytest.mark.parametrize("cache_dir", (".", "./cache"))
def test_cache_dir(tmpdir, cache_dir):
    with tmpdir.as_cwd():
        gridmet = BmiGridmet(start_date="2019-03-14", end_date="2019-03-14", lazy=True, cache_dir=cache_dir)
        assert gridmet.cache_dir.is_absolute()
        assert list(gridmet.cache_dir.glob("*.nc")) == []


def test_cached_data(tmpdir, shared_datadir):
    with tmpdir.as_cwd():
        BmiGridmet("2010-05-22", end_date="2010-05-22", lazy=False, cache_dir=shared_datadir)
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 0


def test_lazy_load(tmpdir):
    with tmpdir.as_cwd():
        gridmet = BmiGridmet("2019-03-14", end_date="2019-03-14", lazy=True, cache_dir=".")
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 0
        gridmet.daily_minimum_temperature
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 1


def test_eager_load(tmpdir):
    with tmpdir.as_cwd():
        BmiGridmet("2019-03-14", end_date="2019-03-14", lazy=False, cache_dir=".")
        assert len(tmpdir.listdir(fil=lambda f: f.ext == ".nc")) == 3
