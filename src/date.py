import json

import click
from dateutil.parser import parse as dateutil_parse
from jinja2 import Environment, FileSystemLoader, StrictUndefined

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
    prop_en = day[0][0].serialize()
    prop_ln = day[0][1].serialize()

    print(_format_as_tex(prop_en, prop_ln))

def _latex_escape(value: str):
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in value)

def _format_as_tex(english: dict, latin: dict) -> str:
    env = Environment(
        loader=FileSystemLoader("src/templates"),
        block_start_string="((*",
        block_end_string="*))",
        variable_start_string="(((",
        variable_end_string=")))",
        comment_start_string="((#",
        comment_end_string="#))",
        undefined=StrictUndefined,
        autoescape=False,
        finalize=_latex_escape
    )
    env.filters["latex"] = _latex_escape
    template = env.get_template("vetus.tex.jinja")

    zipped = list(zip(english, latin))

    return template.render({"propers": zipped})

    

if __name__ == "__main__":
    main()
