"""All day demo, NOTE requires timezone support/local time. See `local_time_pin_demo.py`

NOTE assumes computer time is correct and has correct locale/regional setting.

Under Microsoft Windows; Control Panel\Clock and Region - the time zone setting
Under Linux; check `date +"%Z %z"` and/or `timedatectl |grep 'Time zone'`
"""
# Python 3.x only due to use of:
#  * datetime.isoformat(timespec='milliseconds') - timespec not supported in Python 2.x datetime
#  * datetime.timezone - Python 2 has third-party libs, example; `from dateutil import tz`  # https://github.com/dateutil/dateutil
import datetime
import json
import os
import sys

from pypebbleapi import Timeline  # https://github.com/clach04/pypebbleapi


def datetime2utc_isoformat(in_datetime):
    # `in_datetime` MUST be a UTC datetime (not DATE only)
    # output in javascript isoformat, e.g. "2020-03-29T20:01:00.000Z"

    sample_valid_utc_string = "2022-03-29T20:01:00.000Z"  # match Javascript ISO format EXACTLY    
    utc_date_string = in_datetime.isoformat(timespec='milliseconds')[:len(sample_valid_utc_string) - 1] + 'Z'  # ensures T in there and no space
    return utc_date_string


one_min = datetime.timedelta(minutes=1)

print('Python %s on %s' % (sys.version, sys.platform))

today = datetime.date.today()
print('today')
print(today)
print(today.isoformat())  # 2022-05-14

tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)  # do day math first, before applying timezone to avoid potential DST issues where a day could be more or less than 24 hours
tomorrow = datetime.datetime(tomorrow_date.year, tomorrow_date.month, tomorrow_date.day)

pin_datetime = tomorrow
pin_datetime_as_utc = pin_datetime.astimezone(datetime.timezone.utc)

# basically the same pin as in the utc_pin_demo.py demo, but using local time
my_pin = dict(
    id=datetime2utc_isoformat(pin_datetime_as_utc),
    time=datetime2utc_isoformat(pin_datetime_as_utc),
    "duration"=60 * 24,  # all day
    "layout": {
        "type": "calendarPin",
        "title": "My all day test pin local midnight",
        "tinyIcon": schemas.icon_name_to_path('TIMELINE_CALENDAR')  # "system://images/TIMELINE_CALENDAR"
    }
)
print(json.dumps(my_pin, indent=4))

timeline = Timeline(
    #api_key=my_api_key,  # Needed only if you are going to use shared pins - as of 2022-05 not yet supported by Rebble.io
)

# Send a user pin
timeline.send_user_pin(
    user_token=os.environ['USER_TIMELINE_TOKEN'],
    pin=my_pin,
)

