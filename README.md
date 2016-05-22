# plexmonitor

*Requires*: `python 3.5+`

# Installation and Usage

1. First clone the repo:
```shell
$ git clone https://github.com/jivid/plexmonitor
```

2. Create the virtualenv
```shell
$ cd plexmonitor
$ pyvenv .
$ source bin/activate
```

3. Create the production settings file
```shell
$ cp plexmonitor/settings/github.py plexmonitor/settings/prod.py
$ # Edit the prod.py file with your actual settings
$ export PLEXMONITOR_SETTINGS='plexmonitor.settings.prod'
```

4. And finally, install and run
```shell
$ python setup.py install
$ plexmonitor
```
