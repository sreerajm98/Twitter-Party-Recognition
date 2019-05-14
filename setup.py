"""
Setup partycity as a python package.
Installs all dependencies and installs partycity as a python package.
"""

from setuptools import setup

setup(
    name='partycity',
    version='0.1.0',
    packages=['partycity'],
    include_package_data=True,
    install_requires=[
        'requests',
        'nltk',
        'bs4',
        'pandas',
        'tweepy',
        'textblob',
    ],
    entry_points={
        'console_scripts': [
            'partycity = partycity.__main__:main',
        ]
    },
)
