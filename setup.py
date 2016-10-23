#!/usr/bin/env python
from setuptools import setup


__author__ = 'Yusuke Miyazaki <miyazaki.dev@gmail.com>'
__version__ = '0.1.0'

install_requires = [
    'python-gyazo>=0.11.0,<0.12.0'
]

extras_require = {
    ':python_version=="2.7"': [
        'futures>=3.0.5'
    ]
}

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet',
    'Topic :: Utilities'
]

entry_points = {
    'console_scripts': [
        'gyazo-backup=gyazo_backup:main',
    ],
}

setup(name='python-gyazo-backup',
      version=__version__,
      description='A command-tool for creating backup of Gyazo',
      author='Yusuke Miyazaki',
      author_email='miyazaki.dev@gmail.com',
      url='https://github.com/ymyzk/python-gyazo-backup',
      license='MIT',
      packages=['gyazo_backup'],
      package_data={'gyazo_backup': ['themes/default/*']},
      test_suite='tests',
      install_requires=install_requires,
      extras_require=extras_require,
      classifiers=classifiers,
      entry_points=entry_points)
