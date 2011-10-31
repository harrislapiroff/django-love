#!/usr/bin/env python

from setuptools import setup, find_packages

version = __import__('love').VERSION

setup(
		name='django-love',
		version='.'.join([str(v) for v in version]),
		description='A simple generic upvoting system for Django.',
		packages = find_packages(),
		install_requires = ['django==1.3.1']
	)