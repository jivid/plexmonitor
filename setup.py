from setuptools import setup, find_packages

setup(
    name='plexmonitor',
    version='0.0',
    packages=[
        'plexmonitor',
        'plexmonitor.settings',
        'plexmonitor.lib',
        'plexmonitor.tasks',
    ],
    entry_points={
        'console_scripts': [
            'plexmonitor = plexmonitor.app:main',
        ],
    },
)
