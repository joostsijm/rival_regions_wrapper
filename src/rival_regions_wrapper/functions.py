"""Common functions"""

import re
from datetime import timedelta, timezone

from dateutil import parser


def parse_date(date_string):
    """Try to parse any string to date"""
    date_string = date_string.lower()
    if 'yesterday' in date_string:
        time = re.search(r'\d\d:\d\d', date_string)
        date = parser.parse(time.group(0)) - timedelta(days=1)
    elif 'today' in date_string:
        time = re.search(r'\d\d:\d\d', date_string)
        date = parser.parse(time.group(0))
    elif 'tomorrow' in date_string:
        time = re.search(r'\d\d:\d\d', date_string)
        date = parser.parse(time.group(0)) + timedelta(days=1)
    else:
        date = parser.parse(date_string)
    return date.replace(tzinfo=timezone.utc)
