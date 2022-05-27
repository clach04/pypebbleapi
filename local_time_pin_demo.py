"""Locale time demo that uploads a pin in the same way `utc_pin_demo.py` does but local instead of UTC

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

utc_now = datetime.datetime.utcnow()
print('utc_now')
print(utc_now)
print(datetime2utc_isoformat(utc_now))

local_now = datetime.datetime.now()
print('local_now')
print(local_now)
print(local_now.astimezone(datetime.timezone.utc))
print(local_now.astimezone(datetime.timezone.utc).isoformat(timespec='milliseconds'))


pin_datetime = local_now + (60 * one_min)
pin_datetime_as_utc = pin_datetime.astimezone(datetime.timezone.utc)

# basically the same pin as in the utc_pin_demo.py demo, but using local time
my_pin = dict(
    id=datetime2utc_isoformat(pin_datetime_as_utc),
    time=datetime2utc_isoformat(pin_datetime_as_utc),
    duration=60,  # 60 mins (one hour)
    layout=dict(
        type="genericPin",
        title="MyPin " + pin_datetime.isoformat(),
        tinyIcon="system://images/NOTIFICATION_FLAG",
    ),
    reminders=[
        {
            "time": datetime2utc_isoformat(pin_datetime_as_utc - (15 * one_min)),
            "layout": {
                "type": "genericReminder",
                "tinyIcon": "system://images/TIMELINE_CALENDAR",
                "title": "Pin test - Pin event in 15 minutes"
            }
        },
        {
            "time": datetime2utc_isoformat(pin_datetime_as_utc - (30 * one_min)),
            "layout": {
                "type": "genericReminder",
                "tinyIcon": "system://images/TIMELINE_CALENDAR",
                "title": "Pin test - Pin event in 30 minutes"
            }
        }
    ]
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

