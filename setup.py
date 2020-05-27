from setuptools import setup, find_packages

import versioneer


def read_requirements():
    import os

    path = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(path, "requirements.txt")
    try:
        with open(requirements_file, "r") as req_fp:
            requires = req_fp.read().split()
    except IOError:
        return []
    else:
        return [require.split() for require in requires]


setup(
    name="gridmet_bmi",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Fetch data from the operational National Hydrologic Model",
    author="Eric Hutton",
    author_email="huttone@colorado.edu",
    url="http://csdms.colorado.edu",
    packages=find_packages(exclude=("tests*",)),
    install_requires=[
        "bmipy",
        "click",
        "netcdf4",
        "numpy",
        "pyyaml",
        "requests",
        "xarray",
        "pandas"
    ],
    entry_points={"console_scripts": ["gridmet_bmi=gridmet_bmi.cli:main"]},
)
