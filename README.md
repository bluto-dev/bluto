<h1 align="center"><a href="https://bluto.dev">Bluto</a></h1>
<p align="center"><img src="/bluto/static/markov-portrait-2.jpeg" /></p>

![Build Status](https://github.com/bluto-dev/bluto/actions/workflows/production.yml/badge.svg)

An application that harvests a user's Bluesky history and spits out a faithful
representation of their entire soul!

## Getting started

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements/dev.txt
$ flask run
```

In your browser navigate to localhost:5000/[username] where [username] is the
Bluesky handle you want to generate tweets for.
