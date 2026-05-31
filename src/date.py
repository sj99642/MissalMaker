import datetime
import os
import sys

import click
from dateutil.parser import parse as dateutil_parse

from api import controller

@click.command()
@click.argument("date")
def main(date: str):
    date_parsed = dateutil_parse(date).date()

    # The above creates a combined proper taking into account the temporal and
    # sanctoral cycle
    day = controller.get_proper_by_date(date_parsed, "en")
    


if __name__ == "__main__":
    main()
