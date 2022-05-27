pypebbleapi
============
[![Build Status](https://travis-ci.org/youtux/pypebbleapi.svg?branch=master)](https://travis-ci.org/youtux/pypebbleapi)
[![Documentation Status](https://readthedocs.org/projects/pypebbleapi/badge/?version=latest)](http://pypebbleapi.readthedocs.org/en/latest)

[Rebble.io / Pebble Timeline](https://developer.rebble.io/developer.pebble.com/guides/pebble-timeline/index.html) APIs for python.

[This](https://github.com/clach04/pypebbleapi) is a fork of Alessio Bogon's https://github.com/youtux/pypebbleapi with support for Rebble servers to send pins to the Pebble Timeline for the Pebble smartwatch.
It also integrates all (as of 2022-05-14) the other changes from the other forks found on GitHub.
It has a different version number so as to avoid confusion with the (as of 2022-05) archived repo. Thanks to the Rebble.io maintainers/service timeline support is available for Pebble users! :)

This is a library to ease the access to the Pebble Timeline and validate pins.
It supports Python 2.7, 3.3 and 3.4.

  * [Update](#update)
  * [Install](#install)
  * [Usage](#usage)
  * [Error handling](#error-handling)
  * [Dev Setup](#dev-setup)
    + [Working demos](#working-demos)
  * [Future Ideas](#future-ideas)
  * [Notes](#notes)
  * [Resources](#resources)

Update
-----
Starting from version *1.0.0*, the API has changed. The `Pin` class has
been removed. You should now supply a `dict`, which will be validated before sending.

Install
-------

Just like you install any package:

    $ pip install pypebbleapi

Usage
-----

Here's an example (note for working example see [Working demos](#working-demos) section):
```python
from pypebbleapi import Timeline
import datetime

timeline = Timeline(
    api_key=my_api_key,  # Needed only if you are going to use shared pins
)

my_pin = dict(
    id='123',
    time=datetime.date.today().isoformat(),  # !! This should be a string in the form; "2022-05-25T00:00:00.000Z" - date ONLY is not supported/allowed with Rebble.io - unclear if Pebble supported this (None of the js code indicates this is supported). requests.exceptions.HTTPError: 400 Client Error: The pin object submitted was invalid. for url: https://timeline-api.rebble.io/v1/user/pins/2022-05-16
    layout=dict(
        type="genericPin",
        title="This is a genericPin!",
        tinyIcon="system://images/NOTIFICATION_FLAG",
    )
)

# Send a shared pin
timeline.send_shared_pin(
    topics=['a_topic', 'another_topic'],  # List of the topics
    pin=my_pin,
)

# Send a user pin
timeline.send_user_pin(
    user_token='test-user-token',
    pin=my_pin,
)
```
It is possible that **validation fails** even if the pin is correct (it could happen if Pebble updates the pin specification).
In this case you may want to skip the validation:
```python
timeline.send_user_pin(
    user_token='test-user-token',
    pin=my_pin,
    skip_validation=True,
)
```

Error handling
-----
The API raises errors in case the server is not available or if it returns error codes. You should always enclose calls in `try/except`:
```python
try:
    timeline.send_shared_pin(...)
except Exception as e:
	print(e)
```

If the pin you provided is not valid, a `DocumentError` will be raised:
```python
from pypebbleapi import DocumentError

bad_pin = {}  # Empty pin is not valid
try:
    timeline.send_shared_pin(['a_topic'], bad_pin)
except DocumentError as e:
    print(e)
    print(e.errors)  # e.errors contain a dictionary of the fields that failed the validation
```

Dev Setup
---------

    git clone https://github.com/clach04/pypebbleapi
    pypebbleapi
    pip install -e .

### Working demos

  * [utc_pin_demo.py](utc_pin_demo.py) - Python 3 demo (could be made to work with Python 2 with very little effort)
  * [local_time_pin_demo.py](local_time_pin_demo.py) - Python 3.6+ demo (could be made to work with Python 2 with third party library dateutil)
  * [day_pin_demo.py](day_pin_demo.py) - Python 3.6+ demo (could be made to work with Python 2 with third party library dateutil)

Steps:

1. Install https://apps.rebble.io/en_US/application/5d9ac26dc393f54d6b5f5445 (source available from https://github.com/Willow-Systems/pebble-generate-token/)
2. Generate token on Pebble, copy token from phone via app settings
3. Set operating system environment variable `USER_TIMELINE_TOKEN` to token value, e.g. `set USER_TIMELINE_TOKEN=token` or `export USER_TIMELINE_TOKEN=token`
4. Run demo; `python utc_pin_demo.py`

Future Ideas
------------

TODO ideas:

  * take `datetime2utc_isoformat()` from demos and put into library
  * add datetime support to the schema along with coercion so that (local) date and datetime could be automaticall coerced into a string rather than requiring a string
  * hard fork (and rename to py-pebble-timeline) to use GitHub issue tracking
  * Consider https://github.com/samuelcolvin/pydantic support instead of cerberus

Notes
-----

  * date only string format, old docs indicate date only with no time componentn is sypported - this is not true with Rebble.io servers both of the below appear to be incorrect (or possibly only true for the original Pebble servers?):
      * https://developer.rebble.io/developer.pebble.com/guides/pebble-timeline/timeline-libraries/index.html#pypebbleapi
      * https://github.com/youtux/pypebbleapi
  * shortTitle not supported alone (NOTE this library does not current implement support for shortTitle), https://developer.rebble.io/developer.pebble.com/guides/pebble-timeline/timeline-public/index.html#create-a-pin indicates a title is not needed but a shortTitle alone does not work

Resources
---------

Thanks to the original Python timeline library author Alessio Bogon for https://github.com/youtux/pypebbleapi

Also see other language implementations, including the original Pebble reference implementation in javascript/node:

  * https://github.com/pebble/pebble-api-node
      * https://www.npmjs.com/package/pebble-api
  * https://github.com/Tizzu/RebbleMemos/blob/f36cabab120ebf721db47354bc7b024ed9201085/functions.py#L23
  * MISSING! https://gist.github.com/pebble-gists/6a4082ef12e625d23455
  * https://developer.rebble.io/developer.pebble.com/guides/pebble-timeline/timeline-libraries/index.html
  * https://apps.rebble.io/en_US/application/5d9ac26dc393f54d6b5f5445
  * https://willow.systems/pebble/timeline-tester/
  * https://github.com/Willow-Systems/pebble-timeline-test-server
  * https://github.com/Willow-Systems/pebble-generate-token
  * https://github.com/Willow-Systems/ws-pebble-timeline-services/blob/5767fa574ee9eb927abd0c5812caa02fbc76cb9f/proxyServer/timelineTestProxyServer.js#L447  -- custom implemented API
