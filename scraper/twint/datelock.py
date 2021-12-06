import datetime

import logging as logme

from .tweet import utc_to_local


class Datelock:
    until = None
    since = None
    _since_def_user = None


def convertToDateTime(string):
    dateTimeList = string.split()
    ListLength = len(dateTimeList)
    if ListLength == 2:
        return string
    if ListLength == 1:
        return string + " 00:00:00"
    else:
        return ""


def Set(until, since):
    logme.debug(__name__+':Set')
    d = Datelock()

    if until:
        d.until = datetime.datetime.strptime(convertToDateTime(until), "%Y-%m-%d %H:%M:%S")
        # d.until = utc_to_local(d.until)
    else:
        d.until = datetime.datetime.today()

    if since:
        d.since = datetime.datetime.strptime(convertToDateTime(since), "%Y-%m-%d %H:%M:%S")
        d._since_def_user = True
    else:
        d.since = datetime.datetime.strptime("2006-03-21 00:00:00", "%Y-%m-%d %H:%M:%S")
        d._since_def_user = False

    # d.since = utc_to_local(d.since)
    return d
