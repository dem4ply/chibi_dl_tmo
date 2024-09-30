#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'chibi-dl>=0.1.2', 'undetected-chromedriver>=3.5.2' ]

setup(
    author="dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="command script for download mangas from lectortmo.com or visortmo.com",
    entry_points={
        'console_scripts': [
            'chibi_dl_tmo=chibi_dl_tmo.cli:main',
        ],
    },
    install_requires=requirements,
    license="WTFPL",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chibi_dl_tmo',
    name='chibi_dl_tmo',
    packages=find_packages(include=['chibi_dl_tmo', 'chibi_dl_tmo.*']),
    url='https://github.com/dem4ply/chibi_dl_tmo',
    version='1.1.0',
    zip_safe=False,
)
