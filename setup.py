#!/usr/bin/env python

from setuptools import setup

setup(

    name="teblr",
    version="0.0.1.1",
    description="Tumblr on command line",
    long_description="Tumblr on command line for Terminal and Linux lovers.",
    keywords="tumblr terminal commandline blogging",
    author="Vijay Kumar",
    author_email="nvijaykumar2012@gmail.com",
    url="https://github.com/vijaykumarhackr/teblr/",
    packages = ['teblr'],
    license = "GPL 3",

    # test_suite='nose.collector',

    entry_points = {
        'console_scripts' : ['tumblr=teblr.main:main'],
        },


    install_requires = [
        'pytumblr',
    ],

    # include_package_data=True,

    # tests_require=[
    #     'nose',
    #     'nose-cov',
    #     'mock'
    # ]

)
