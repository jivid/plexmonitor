# plexmonitor

*Requires*: `python 3.5+`

# Installation and Usage

First clone the repo:
```shell
$ git clone https://github.com/jivid/plexmonitor
```

Create the virtualenv
```shell
$ cd plexmonitor
$ pyvenv .
$ source bin/activate
```

Create the production settings file
```shell
$ cp plexmonitor/settings/github.py plexmonitor/settings/prod.py
$ # Edit the prod.py file with your actual settings
$ export PLEXMONITOR_SETTINGS='plexmonitor.settings.prod'
```

And finally, install and run
```shell
$ python setup.py install
$ plexmonitor
```
