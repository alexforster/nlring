# -*- coding: UTF-8 -*-
#
# Copyright © 2017 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.
#

from setuptools import setup


setup(
    name='nlring',
    version='1.0.0',
    author='Alex Forster',
    author_email='alex@alexforster.com',
    maintainer='Alex Forster',
    maintainer_email='alex@alexforster.com',
    url='https://github.com/AlexForster/nlring',
    description='NLNOG Ring task execution library',
    license='3-Clause ("New") BSD license',
    download_url='https://pypi.python.org/pypi/nlring',
    packages=['nlring'],
    package_dir={'nlring': './nlring'},
    package_data={'nlring': [
        './README',
        './README.rst',
        './LICENSE',
    ]},
    install_requires=[
        'inparallel<1.1.0',
        'requests<2.13.0',
        'ptyprocess<0.6.0',
        'pyte<0.6.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
)
