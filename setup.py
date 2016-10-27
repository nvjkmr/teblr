#!/usr/bin/env python

from setuptools import setup

setup(

    name="teblr",
    version="0.0.0",
    description="Tumblr on command line for Terminal and Linux lovers.",
    author="Vijay Kumar",
    author_email="nvijaykumar2012@gmail.com",
    url="https://github.com/vijaykumarhackr/teblr/",
    packages = ['teblr'],
    license = "LICENSE",

    # test_suite='nose.collector',

    install_requires = [
        'pytumblr',
    ],

    # tests_require=[
    #     'nose',
    #     'nose-cov',
    #     'mock'
    # ]

)
