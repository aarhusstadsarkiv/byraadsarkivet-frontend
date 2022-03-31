from typing import Dict, Any
from datasette import hookimpl


@hookimpl
def extra_template_vars(request) -> Dict[str, Any]:
    # Custom template variables
    vars: Dict[str, Any] = {}

    # the latest year of the db. Currently 2021
    vars["to_year"] = 2021
    vars["from_year"] = 1997

    # human dates
    vars["months"] = {
        "01": "Jan",
        "02": "Feb",
        "03": "Mar",
        "04": "Apr",
        "05": "Maj",
        "06": "Jun",
        "07": "Jul",
        "08": "Aug",
        "09": "Sep",
        "10": "Okt",
        "11": "Nov",
        "12": "Dec",
    }

    vars["previous_fora"] = {
        "32": {
            "from": "2017",
            "to": "2017",
            "label": "Udvalget for Frivillighed og Samskabelse (2017)",
        },
        "47": {
            "from": "2010",
            "to": "2011",
            "label": "Udvalget vedrørende Byrådets Arbejdsforhold (2010-2011)",
        },
        "24": {
            "from": "2006",
            "to": "2017",
            "label": "Socialudvalget (2006-2017)",
        },
        "1": {
            "from": "2006",
            "to": "2017",
            "label": "Beskæftigelsesudvalget (2006-2017)",
        },
        "33": {
            "from": "1998",
            "to": "2005",
            "label": "Udvalget for Kommunale Driftsvirksomheder (1998-2005)",
        },
        "37": {
            "from": "1998",
            "to": "2005",
            "label": "Udvalget for Skoler og Kultur (1998-2005)",
        },
        "39": {
            "from": "1998",
            "to": "2005",
            "label": "Udvalget for Sociale og Beskæftigelsesmæssige \
            Anliggender samt Børn og Unge (1998-2005)",
        },
        "43": {
            "from": "1997",
            "to": "2005",
            "label": "Udvalget for Tekniske Anliggender (1997-2005)",
        },
        "31": {
            "from": "1997",
            "to": "1997",
            "label": "Udvalget for Fast Ejendom og Grønne Områder (1997)",
        },
        "34": {
            "from": "1997",
            "to": "1997",
            "label": "Udvalget for Kommunale Forsyningsvirksomheder (1997)",
        },
        "36": {
            "from": "1997",
            "to": "1997",
            "label": "Udvalget for Kulturelle Anliggender (1997)",
        },
        "38": {
            "from": "1997",
            "to": "1997",
            "label": "Udvalget for Sociale Anliggender (1997)",
        },
    }
    vars["current_fora"] = {
        "13": {"from": "1997", "to": "2021", "label": "Aarhus Byråd (1997-)"},
        "20": {"from": "1997", "to": "2021", "label": "Magistraten (1997-)"},
        "14": {
            "from": "2006",
            "to": "2021",
            "label": "Børn og Unge-udvalget (2006-)",
        },
        "19": {
            "from": "2006",
            "to": "2021",
            "label": "Kulturudvalget (2006-)",
        },
        "23": {
            "from": "2018",
            "to": "2021",
            "label": "Social- og Beskæftigelsesudvalget (2018-)",
        },
        "27": {
            "from": "1998",
            "to": "2021",
            "label": "Sundheds- og Omsorgsudvalget (1998-)",
        },
        "28": {
            "from": "2006",
            "to": "2021",
            "label": "Teknisk Udvalg (2006-)",
        },
        "49": {
            "from": "2006",
            "to": "2021",
            "label": "Økonomiudvalget (2006-)",
        },
        "16": {
            "from": "2008",
            "to": "2021",
            "label": "Fælles udvalgsmøde (2008-)",
        },
    }

    vars["all_fora"] = {
        "13": "Aarhus Byråd",
        "20": "Magistraten",
        "14": "Børn og Unge-udvalget",
        "19": "Kulturudvalget",
        "23": "Social- og Beskæftigelsesudvalget",
        "27": "Sundheds- og Omsorgsudvalget",
        "28": "Teknisk Udvalg",
        "49": "Økonomiudvalget",
        "16": "Fælles udvalgsmøde",
        "18": "Internationaliseringsudvalget",
        "21": "Medborgerskabsudvalget",
        "26": "Styringsudvalget",
        "25": "Styreforms- og Strukturudvalget",
        "32": "Udvalget for Frivillighed og Samskabelse",
        "47": "Udvalget vedrørende Byrådets Arbejdsforhold",
        "24": "Socialudvalget",
        "1": "Beskæftigelsesudvalget",
        "33": "Udvalget for Kommunale Driftsvirksomheder",
        "37": "Udvalget for Skoler og Kultur",
        "39": "Udvalget for Sociale og Beskæftigelsesmæssige Anliggender \
            samt Børn og Unge",
        "43": "Udvalget for Tekniske Anliggender",
        "31": "Udvalget for Fast Ejendom og Grønne Områder",
        "34": "Udvalget for Kommunale Forsyningsvirksomheder",
        "36": "Udvalget for Kulturelle Anliggender",
        "38": "Udvalget for Sociale Anliggender",
    }

    return vars
