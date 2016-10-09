# -*- coding: utf-8 -*-
####################################################################################################
##                                                                                                ##
##            Copyright (C) 2016 William McKIE                                                    ##
##                                                                                                ##
##            This program is free software: you can redistribute it and/or modify                ##
##            it under the terms of the GNU General Public License as published by                ##
##            the Free Software Foundation, either version 3 of the License, or                   ##
##            (at your option) any later version.                                                 ##
##                                                                                                ##
##            This program is distributed in the hope that it will be useful,                     ##
##            but WITHOUT ANY WARRANTY; without even the implied warranty of                      ##
##            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                       ##
##            GNU General Public License for more details.                                        ##
##                                                                                                ##
##            You should have received a copy of the GNU General Public License                   ##
##            along with this program.  If not, see <http://www.gnu.org/licenses/>.               ##
##                                                                                                ##
####################################################################################################
import sys
from pathlib import Path

from setuptools import find_packages, setup

import stoiridhtools

if sys.version_info < (3, 5):
    print('ERROR: Stòiridh Tools requires at least Python 3.5 to run.')
    sys.exit(1)

if not (sys.platform.startswith('linux') or sys.platform.startswith('win32')):
    print('ERROR: Stòiridh Tools is only available on GNU/Linux or Windows.')
    sys.exit(1)


# get the long description from the README.rst file
readme = Path('README.rst').resolve()

with readme.open(encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='stoiridhtools',
    version=stoiridhtools.__version__,
    license='GPLv3+',
    author='Stòiridh Project',
    author_email='stoiridh-project@googlegroups.com',
    url='https://github.com/StoiridhProject/StoiridhTools',
    description='Enhance your Qbs-based projects',
    long_description=long_description,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    platforms='linux win32',
    keywords='development build-tools qbs stoiridhtools',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'stoiridhtools=stoiridhtools:main',
        ],
    },
)
