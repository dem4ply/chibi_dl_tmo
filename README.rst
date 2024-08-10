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
	pip install -e git+https://github.com/jdholtz/undetected-chromedriver.git@29551bd27954dacaf09864cf77935524db642c1b#egg=undetected_chromedriver

is going to add the command chibi_dl_tmo


===========
how to used
===========


.. code-block:: text

	usage: chibi_dl_tmo [-h] [--only_print] [--only_metadata] [--only_links] [--user USER] [--password PASSWORD] [--log_level LOG_LEVEL] [-o DOWNLOAD_PATH]
                    [-config_site CONFIG_SITE]
                    site [site ...]
	descarga mangas
	positional arguments:
	  site                  urls de las series que se quieren descargar
	options:
	  -h, --help            show this help message and exit
	  --only_print          define si silo va a imprimir la lista de links o episodios
	  --only_metadata       se define si solo se queire recolectar los datos y no descargar
	  --only_links          si se usa solo imprimira las urls
	  --user USER, -u USER  usuario del sitio
	  --password PASSWORD, -p PASSWORD
	                        contrasenna del sitio
	  --log_level LOG_LEVEL
	                        nivel de log
	  -o DOWNLOAD_PATH, --output DOWNLOAD_PATH
	                        ruta donde se guardara el video o manga
	  -config_site CONFIG_SITE
	                        python, yaml o json archivo con el usuario y password de cada sitio

.. code-block:: bash

	chibi_dl -o /path/to/save/serie "https://tmofans.com/library/manga/13698/komi-san-wa-komyushou-desu"

for get all the list of pending, follow and read in tmo fans
need the user and password for do the login and retrive the list of links
and donwload all the series

.. code-block:: bash

	chibi_dl --only_print --only_links -p $PASSWORD -u $USER https://tmofans.com/profile/read https://tmofans.com/profile/pending  https://tmofans.com/profile/follow > links_of_mangas
	chibi_dl -o /path/to/save/series @links_of_mangas

can add a config file to set the default download folder

.. code-block:: bash

	echo <<EOF
	from chibi.config import configuration
	configuration.chibi_dl_tmo.download_path = '~/path/mangas'
	EOF > ~/.config/chibi/chibi_dl_tmo.py
	chibi_dl @links_of_mangas
