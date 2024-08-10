# -*- coding: utf-8 -*-
"""Console script for chibi_dl_tmo."""
import argparse
import sys
import json
import sys
import logging
import random
from argparse import ArgumentParser
import urllib3

from chibi.file import Chibi_path
from chibi.config import basic_config, load as load_config
from chibi.config import default_file_load, configuration

from chibi_dl_tmo import TMO_fans

default_file_load( 'chibi_dl_tmo.py', touch=True )
logger_formarter = '%(levelname)s %(name)s %(asctime)s %(message)s'


parser = ArgumentParser(
    description="descarga mangas", fromfile_prefix_chars='@'
)

parser.add_argument(
    "sites", nargs='+', metavar="site",
    help="urls de las series que se quieren descargar" )

parser.add_argument(
    "--only_print", dest="only_print", action="store_true",
    help="define si silo va a imprimir la lista de links o episodios"
)

parser.add_argument(
    "--only_metadata", dest="only_metadata", action="store_true",
    help="se define si solo se queire recolectar los datos y no descargar"
)

parser.add_argument(
    "--only_links", dest="only_print_links", action="store_true",
    help="si se usa solo imprimira las urls"
)

parser.add_argument(
    "--user", '-u', dest="user", default="",
    help="usuario del sitio" )

parser.add_argument(
    "--password", '-p', dest="password", default="",
    help="contrasenna del sitio" )

parser.add_argument(
    "--log_level", dest="log_level", default="INFO",
    help="nivel de log",
)

default_download_path=configuration.chibi_dl_tmo.get( 'download_path' )
if default_download_path:
    parser.add_argument(
        "-o", "--output", type=Chibi_path, dest="download_path",
        default=default_download_path,
        help="ruta donde se guardara el video o manga" )
else:
    parser.add_argument(
        "-o", "--output", type=Chibi_path, dest="download_path", required=True,
        help="ruta donde se guardara el video o manga" )

parser.add_argument(
    "-config_site", type=Chibi_path, dest="config_site",
    help="python, yaml o json archivo con el usuario y password de cada sitio"
)

parser.add_argument(
    "--amount", type=int, dest="amount", default=None,
    help="cantidad de episodios que descargara"
)


def main():
    """Console script for chibi_dl_tmo."""
    # tmo falla de vez en cuando con el https o siempre
    urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )
    args = parser.parse_args()
    args.download_path
    basic_config( args.log_level )

    tmo_fans = TMO_fans( user=args.user, password=args.password, )

    for site in args.sites:
        tmo_fans.append( site )

    if args.only_print:
        if args.only_print_links:
            for serie in tmo_fans.series:
                print( serie.url )
    else:
        for serie in tmo_fans.series:
            serie.download( args.download_path, amount=args.amount )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
