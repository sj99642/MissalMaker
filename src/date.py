import json
from copy import deepcopy
import re

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
    prop_en = _proper_latexification(day[0][0].serialize())
    prop_ln = _proper_latexification(day[0][1].serialize())

    print(_format_as_tex(prop_en, prop_ln))

def _latex_escape(value: str):
    # replacements = {
    #     "\\": r"\textbackslash{}",
    #     "&": r"\&",
    #     "%": r"\%",
    #     "$": r"\$",
    #     "#": r"\#",
    #     "_": r"\_",
    #     "{": r"\{",
    #     "}": r"\}",
    #     "~": r"\textasciitilde{}",
    #     "^": r"\textasciicircum{}",
    # }
    # return "".join(replacements.get(ch, ch) for ch in value)
    return value

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


def _proper_latexification(proper: dict) -> dict:
    """
    Does the following things:
    * Removes "Continuation of the Holy Gospel..." and "Lesson from..." from the Gospel and Epistle
    * Replace bolded text using `**` with `\\textbf{}`
    """

    # We make a new copy, mutate that copy in place, then return it
    new_proper = deepcopy(proper)

    # Remove the introductory text from the Gospel
    gospel_dict = [d for d in new_proper if d["id"] == "Evangelium"][0]
    gospel_dict["body"] = "\n".join(gospel_dict["body"].split("\n")[1:])

    # Remove the introductory text from the Epistle
    epistle_dict = [d for d in new_proper if d["id"] == "Lectio"][0]
    epistle_dict["body"] = "\n".join(epistle_dict["body"].split("\n")[1:])

    # Modify bolded text
    for d in new_proper:
        d["body"] = re.sub(r"\*(.+)\*", r"\\textbf{\1}", d["body"])

    return new_proper


    

if __name__ == "__main__":
    main()
