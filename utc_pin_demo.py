# Python 3.x only due to use of datetime.isoformat(timespec='milliseconds') - timespec not supported in Python 2.x datetime
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
print(today)
print(today.isoformat())  # 2022-05-14

utc_now = datetime.datetime.utcnow()

print(utc_now)
print(datetime2utc_isoformat(utc_now))

pin_datetime = utc_now + (60 * one_min)

my_pin = dict(
    id=datetime2utc_isoformat(pin_datetime),
    time=datetime2utc_isoformat(pin_datetime),
    layout=dict(
        type="genericPin",
        title="MyPin",
        tinyIcon="system://images/NOTIFICATION_FLAG",
    ),
    reminders=[
        {
            "time": datetime2utc_isoformat(pin_datetime - (15 * one_min)),
            "layout": {
                "type": "genericReminder",
                "tinyIcon": "system://images/TIMELINE_CALENDAR",
                "title": "Pin test - Pin event in 15 minutes"
            }
        },
        {
            "time": datetime2utc_isoformat(pin_datetime - (30 * one_min)),
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

