<h1 align="center"><a href="https://twitkov.club">Twitkov</a></h1>
<p align="center"><img src="/static/markov-portrait-2.jpeg" /></p>

[![Build Status](https://travis-ci.org/brianshortnh/twitkov.svg?branch=master)](https://travis-ci.org/brianshortnh/twitkov)

An application that harvests a user's Twitter history and spits out a faithful
representation of their entire soul!

## Getting started

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ FLASK_APP=markov_flask.py flask run
```

In your browser navigate to localhost:5000/[username] where [username] is the
Twitter handle you want to generate tweets for.
