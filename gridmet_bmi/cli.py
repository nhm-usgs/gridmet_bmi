import datetime
import sys

import click

from gridmet_bmi import __version__
from gridmet_bmi.gridmet import Gridmet


def yesterday():
    return datetime.date.isoformat(datetime.date.today() - datetime.timedelta(days=1))


def validate_date(date_string):
    try:
        date = datetime.date.fromisoformat(date_string)
    except ValueError:
        raise click.BadParameter("not an ISO formatted date ({0})".format(date_string))
    else:
        return date


@click.command()
@click.version_option(version=__version__)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help=(
        "Don't emit non-error messages to stderr. Errors are still emitted, "
        "silence those with 2>/dev/null."
    ),
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Also emit status messages to stderr."
)
@click.option(
    "--start",
    metavar="YYYY-MM-DD",
    default=yesterday,
    help="Start date",
    show_default="yesterday",
)
@click.option(
    "--end",
    metavar="YYYY-MM-DD",
    default=yesterday,
    help="End date",
    show_default="yesterday",
)
@click.argument("var", type=click.Choice(["tmin", "tmax", "precip"]))
def main(quiet, verbose, config_file, start, end, var):
    print("test")
    # fetcher = Gridmet(start, end_date=end, hrumap=hrumap, hru_id=hru_ids, wght_file=wght_file)
    fetcher = Gridmet(config_file=config_file)
    print(getattr(fetcher, var))


if __name__ == "__main__":
    sys.exit(main())
