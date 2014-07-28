#!/usr/bin/env python

import os

from setuptools import setup, find_packages

from version import get_git_version
VERSION, SOURCE_HASH = get_git_version()
PROJECT = 'streamcorpus-elasticsearch'
URL = 'https://github.com/trec-kba'
AUTHOR = 'Diffeo, Inc.'
AUTHOR_EMAIL = 'support@diffeo.com'
DESC = 'Tool for loading streamcorpus.StreamItems into ElasticSearch'
LICENSE ='MIT/X11 license http://opensource.org/licenses/MIT'

def read_file(file_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
    )
    return open(file_path).read()

setup(
    name=PROJECT,
    version=VERSION,
    #source_label=SOURCE_HASH,
    license=LICENSE,
    description=DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(),
    # We can select proper classifiers later
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',  ## MIT/X11 license http://opensource.org/licenses/MIT
    ],
    tests_require=[
    ],
    install_requires=[
        'yakonfig >= 0.5.0',
        'rejester',
        'kvlayer >= 0.4.0',
        'dblogger >= 0.4.0',
        'streamcorpus >= 0.3.27',
        'elasticsearch',
    ],
    include_package_data = True,
)
