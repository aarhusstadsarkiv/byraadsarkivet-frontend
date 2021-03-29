import json
import re
from datetime import datetime
from jinja2 import Markup
from datasette import hookimpl


def highlight(value, query_string=None):
    def wrapper(matchobj):
        return "<mark class='highlight'>" + matchobj.group(0) + "</mark>"

    if not isinstance(query_string, str) or query_string == "":
        return value
    if not isinstance(value, str) or value == "":
        return value

    # 'å' is encoded wrongly in the data from the db (or through Jinja).
    # Therefore we replace any correct 'å' from the query-params, with
    # the wrong one, to enable pattern-matching and thereby highlighting
    replaced_query = query_string.encode().replace(b"\xc3\xa5", b"a\xcc\x8a")

    # return value.encode(), replace_val  # , value.encode().hex()
    # return (
    #     "From web-query: "
    #     + json.dumps(query_string)
    #     + ", from sourcecode: "
    #     + json.dumps("å")
    # )
    # query_string = "å"
    # value = "Skæring, Ærø, Ågaden, Skåde, å, sådan, ø, sø"

    regex_list = ["\\b(" + x + ")" for x in replaced_query.decode().split(" ")]
    regex_obj = re.compile(r"|".join(regex_list), flags=re.IGNORECASE)
    highlights = regex_obj.sub(wrapper, value)
    return Markup(highlights)


def load_json(value):
    if not isinstance(value, str):
        return None
    try:
        data = json.loads(value)
    except ValueError:
        return None

    if not isinstance(data, (dict, list)):
        return None

    return data


def localize_date(value):
    def months(month):
        months = {
            "01": "januar",
            "02": "februar",
            "03": "marts",
            "04": "april",
            "05": "maj",
            "06": "juni",
            "07": "juli",
            "08": "august",
            "09": "september",
            "10": "oktober",
            "11": "november",
            "12": "december",
        }
        return months.get(month)

    if not isinstance(value, str):
        return value
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return value

    day = int(value[-2:])
    month = months(value[5:7])
    year = value[0:4]
    return f"{day}. {month} {year}"


@hookimpl
def prepare_jinja2_environment(env):
    env.filters["highlight"] = highlight
    env.filters["loadjson"] = load_json
    env.filters["localize"] = localize_date
