# -*- coding: utf-8 -*-
import datetime
import re
import urllib
from pathlib import Path

import requests
import xarray as xr
import yaml


class Gridmet:
    SCHEME = "http"
    NETLOC = "thredds.northwestknowledge.net:8080"
    PATH = {
        "daily_maximum_temperature": "thredds/ncss/agg_met_tmmx_1979_CurrentYear_CONUS.nc",
        "daily_minimum_temperature": "thredds/ncss/agg_met_tmmn_1979_CurrentYear_CONUS.nc",
        "precipitation_amount": "thredds/ncss/agg_met_pr_1979_CurrentYear_CONUS.nc",
    }

    def __init__(
        self,
        start_date="2019-03-15",
        end_date="2019-03-21",
        config_file=None,
        lazy=True,
        cache_dir=None,
    ):
        self._wghts = None
        self._wghts_id = None
        self._start_date = start_date
        self._end_date = end_date

        print(yaml.dump(config_file))
        if config_file is not None:
            with open(config_file, "r") as fp:
                parameters = yaml.safe_load(fp)
            for key, value in parameters.items():
                setattr(self, key, value)
        else:
            self._start_date = Gridmet.datetime_or_yesterday(start_date)
            self._end_date = Gridmet.datetime_or_yesterday(end_date)

        if self._start_date > self._end_date:
            raise ValueError(
                "start date ({0}) must be before end date ({1})".format(
                    self._start_date, self._end_date
                )
            )
        if self._end_date > datetime.date.today():
            raise ValueError(
                "end date cannot be a future date ({0} > {1}".format(
                    self._end_date, datetime.date.today()
                )
            )
        self._delta = self._end_date - self._start_date
        self._m_tmin_data = None
        self._m_tmax_data = None
        self._m_prcp_data = None

        if cache_dir is None:
            cache_dir = Path("~/.gridmet")
        self._cache_dir = Path(cache_dir).expanduser().resolve()

        self._dataset = None
        if not lazy:
            for name in self.PATH:
                self._lazy_load(name)

        self.dt = 1.0
        self.time = 0.0
        self.end = float(self._delta.days + 1)

    @staticmethod
    def clear_cache(cache_dir=None):
        for fname in Gridmet.list_cache(cache_dir=cache_dir):
            fname.unlink()

    @staticmethod
    def list_cache(cache_dir=None):
        if cache_dir is None:
            cache_dir = Path("~/.gridmet")
        cache_dir = Path(cache_dir).expanduser().resolve()

        pattern = r"(?P<var>[a-z_]*)_(?P<start>[0-9\-]*)_(?P<end>[0-9\-]*)\.nc"

        cached_files = []
        for fname in [p.name for p in cache_dir.glob("*.nc")]:
            match = re.match(pattern, fname)
            if match and match.group("var") in Gridmet.PATH:
                try:
                    datetime.date.fromisoformat(match.group("start"))
                    datetime.date.fromisoformat(match.group("end"))
                except ValueError:
                    pass
                else:
                    cached_files.append(cache_dir / fname)

        return cached_files

    @staticmethod
    def datetime_or_yesterday(val):
        if val is None:
            return datetime.date.today() - datetime.timedelta(days=1)
        elif isinstance(val, str):
            return datetime.date.fromisoformat(val)
        else:
            return val

    @classmethod
    def from_today(cls, days, lazy=True):
        if days <= 0:
            raise ValueError("number of days must be positive ({0})".format(days))

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)

        return cls(start_date, end_date, lazy=lazy)

    @property
    def cache_dir(self):
        return self._cache_dir

    @property
    def start_date(self):
        return str(self._start_date)

    @property
    def end_date(self):
        return str(self._end_date)

    @property
    def dataset(self):
        return self._dataset

    def _fetch_and_open(self, name):
        self._cache_dir.mkdir(exist_ok=True)
        return xr.open_dataset(
            Gridmet.fetch_var(
                name, self._start_date, self._end_date, cache_dir=self._cache_dir
            )
        )

    def _lazy_load(self, name):
        if self._dataset is None:
            self._dataset = self._fetch_and_open(name)

        try:
            self._dataset[name]
        except KeyError:
            self._dataset = self._dataset.merge(self._fetch_and_open(name))

        return self._dataset[name]

    @property
    def tmax(self):
        tname = "daily_maximum_temperature"
        ds = self._lazy_load(tname)
        return ds

    @property
    def tmin(self):
        tname = "daily_minimum_temperature"
        ds = self._lazy_load(tname)
        return ds

    @property
    def prcp(self):
        tname = "precipitation_amount"
        ds = self._lazy_load(tname)
        return ds

    @classmethod
    def fetch_var(cls, name, start_date, end_date=None, cache_dir="."):
        if name not in cls.PATH:
            raise ValueError(
                "name not understood ({0} not in {1})".format(name, ", ".join(cls.PATH))
            )

        end_date = end_date or datetime.date.today()
        fname = Path(cache_dir) / "{var}_{start}_{end}.nc".format(
            var=name, start=start_date, end=end_date
        )

        if not fname.is_file():
            params = {
                "var": name,
                "north": "49.4000",
                "west": "-124.7666",
                "east": "-67.0583",
                "south": "25.0666",
                "disableLLSubset": "on",
                "disableProjSubset": "on",
                "horizStride": "1",
                "time_start": start_date.strftime("%Y-%m-%d") + "T00:00:00Z",
                "time_end": end_date.strftime("%Y-%m-%d") + "T00:00:00Z",
                "timeStride": "1",
                "accept": "netcdf",
            }

            response = requests.get(cls.data_url(name), params=params)
            response.raise_for_status()

            with fname.open("wb") as fp:
                fp.write(response.content)

        return fname.absolute()

    @classmethod
    def data_url(cls, name):
        return urllib.parse.urlunparse(
            (cls.SCHEME, cls.NETLOC, cls.PATH[name], "", "", "")
        )

    def update(self):
        self.time += self.dt
