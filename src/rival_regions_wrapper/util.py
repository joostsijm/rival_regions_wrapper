"""
Common functions and datastructures that modules might need
"""

import re
from datetime import timedelta, timezone

from dateutil import parser


ITEM_KEYS = {
    "oil": 3,
    "ore": 4,
    "uranium": 11,
    "diamonds": 15,
    "liquid_oxygen": 21,
    "helium-3": 24,
    "rivalium": 26,
    "antirad": 13,
    "energy_drink": 17,
    "spacerockets": 20,
    "lss": 25,
    "tanks": 2,
    "aircrafts": 1,
    "missiles": 14,
    "bombers": 16,
    "battleships": 18,
    "laser_drones": 27,
    "moon_tanks": 22,
    "space_stations": 23,
}


def parse_date(date_string):
    """Try to parse any string to date"""
    date_string = date_string.lower()
    if "yesterday" in date_string:
        time = re.search(r"\d\d:\d\d", date_string)
        date = parser.parse(time.group(0)) - timedelta(days=1)
    elif "today" in date_string:
        time = re.search(r"\d\d:\d\d", date_string)
        date = parser.parse(time.group(0))
    elif "tomorrow" in date_string:
        time = re.search(r"\d\d:\d\d", date_string)
        date = parser.parse(time.group(0)) + timedelta(days=1)
    else:
        date = parser.parse(date_string)
    return date.replace(tzinfo=timezone.utc)
