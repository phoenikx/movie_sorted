# Movie Sorted

> Movie bookings made easy

Steps to run any script, say hall_opening_alerter.py:

1. Make a virtual environment and activate it.

1. Install dependencies by running ``pip3 install -r requirements.txt``

1. Export 3 environment variables: *SENDGRID_API_KEY*, *FROM_EMAIL* and *TZ* as the scripts use the same.

> For running hall_opening_alerter.py

1. ```python3 hall_opening_alerter/hall_opening_alerter.py movie_name location movie_id emails dates_in_yyyymmdd_format(optional)```

For example:- 

```python3 hall_opening_alerter/hall_opening_alerter.py avengers-endgame bengaluru movie-bang-ET00090482-MT central,soul,space xyz@gmail.com```


> For running movie_opening_alerter.py

1. 

```python3 movie_opening_alerter/movie_opening_alerter.py movie_name location movie_id emails dates_in_yyyymmdd_format```

For example-

```python3 movie_opening_alerter/movie_opening_alerter.py avengers-endgame hyderabad movie-hyd-ET00090482-MT xyz@gmail.com,abc@gmail.com 20190426,20190427```