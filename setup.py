#!/usr/bin/env python
"""
Alternative Class Based Views
=============================

:copyright: (c) 2012 by Linovia.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


tests_require = [
    'mock',
]

install_requires = [
    'Django>=1.4',
]

setup(
    name='acbv',
    version='0.0.1',
    author='Xavier Ordoquy',
    author_email='xordoquy@linovia.com',
    url='http://github.com/linovia/acbv',
    description='Alternative to Django class based views.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python'
        'Environment :: Web Environment',
    ],
)
