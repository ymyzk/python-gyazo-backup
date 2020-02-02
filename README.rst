python-gyazo-backup
===================
.. image:: https://badge.fury.io/py/python-gyazo-backup.svg
   :target: https://pypi.python.org/pypi/python-gyazo-backup/
   :alt: PyPI Version
.. image:: https://img.shields.io/pypi/pyversions/python-gyazo-backup.svg
   :target: https://pypi.python.org/pypi/python-gyazo-backup/
   :alt: PyPI Python versions
.. image:: https://travis-ci.org/ymyzk/python-gyazo-backup.svg?branch=master
   :target: https://travis-ci.org/ymyzk/python-gyazo-backup
   :alt: Build Status

A command-tool for creating backup of Gyazo

Requirements
------------
* Python 3.5+

Installation
------------
.. code-block:: shell

   pip install python-gyazo-backup

Usage
-----
At first, you must create an application and get an access token from https://gyazo.com/oauth/applications

Then, download all images with ``gyazo-backup`` command:

.. code-block:: shell

   gyazo-backup --token <API_ACCESS_TOKEN> <DESTINATION_DIR>


You can see all downloaded images with your favorite web browser.
Please open ``<DESTINATION_DIR>/index.html``.

.. image:: https://github.com/ymyzk/python-gyazo-backup/raw/master/docs/images/backup_example.jpg

License
-------
MIT License. Please see `LICENSE`_.

.. _LICENSE: LICENSE
