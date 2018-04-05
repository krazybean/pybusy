"""
Cursor glamor prettiness for bash


"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pybusy',
    version='0.0.1',
    description='Bash progress decoration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/krazybean/pybusy',
    author='krazybean',
    author_email='krazybean@gmail.com',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='python3 bash progress',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['cursor', 'ansicolors']
)
