============
chibi_dl_tmo
============


.. image:: https://img.shields.io/pypi/v/chibi_dl_tmo.svg
        :target: https://pypi.python.org/pypi/chibi_dl_tmo

.. image:: https://img.shields.io/travis/dem4ply/chibi_dl_tmo.svg
        :target: https://travis-ci.org/dem4ply/chibi_dl_tmo

.. image:: https://readthedocs.org/projects/chibi-dl-tmo/badge/?version=latest
        :target: https://chibi-dl-tmo.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




command script for download mangas from lectortmo.com


* Free software: WTFPL
* Documentation: https://chibi-dl-tmo.readthedocs.io.


Features
--------

is a command line tool for download series from tmofans.com

for the mangas from tmofans is going to compress all the images in a
zip and rename the extencion to cbz


=======
install
=======


.. code-block:: bash

	pip install chibi_dl_tmo

is going to add the command chibi_dl_tmo


===========
how to used
===========


.. code-block:: text

	usage: chibi_dl [-h] [--user USER] [--password PASSWORD]
						[--resoulution QUALITY]
						site [site ...] download_path

	descarga mangas

	positional arguments:
	site                  urls de las series que se quieren descargar
	download_path         lugar de descarga

	optional arguments:
	-h, --help            show this help message and exit
	--user USER, -u USER  usuario del sitio
	--password PASSWORD, -p PASSWORD
									contrasenna del sitio
	--resoulution QUALITY, -q QUALITY
									resolucion a descargar

.. code-block:: bash

	chibi_dl -o /path/to/save/serie "https://tmofans.com/library/manga/13698/komi-san-wa-komyushou-desu"

for get all the list of pending, follow and read in tmo fans
need the user and password for do the login and retrive the list of links
and donwload all the series

.. code-block:: bash

	chibi_dl --only_print --only_links -p $PASSWORD -u $USER https://tmofans.com/profile/read https://tmofans.com/profile/pending  https://tmofans.com/profile/follow > links_of_mangas
	chibi_dl -o /path/to/save/series @links_of_mangas
