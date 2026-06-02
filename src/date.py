import json

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

    # This should contain two propers, the english and the latin
    assert len(day) == 1
    assert len(day[0]) == 2
    prop_en = day[0][0]
    prop_ln = day[0][1]

    # I've checked that, at least for 2026, this always matches the same IDs together
    for part_en, part_ln in zip(prop_en.serialize(), prop_ln.serialize()):
        assert part_en["id"] == part_ln["id"]

        print(f"## {part_en['label']}")
        print(f"{part_en['body']}")
        print()
    

if __name__ == "__main__":
    main()
