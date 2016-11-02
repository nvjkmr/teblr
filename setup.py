#!/usr/bin/env python

from setuptools import setup

setup(

    name="teblr",
    version="0.0.2",
    description="Tumblr on command line",
    long_description="Tumblr on command line written in Python for Terminal and Linux lovers.",
    keywords="tumblr terminal commandline blogging linux",
    author="Vijay Kumar",
    author_email="nvijaykumar2012@gmail.com",
    url="http://nvijaykumar.me/teblr/",
    packages = ['teblr'],
    license = "Apache 2.0",

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
