import logging
import re
import shutil
import time

from bs4 import BeautifulSoup
from chibi.file import Chibi_path
from chibi_requests import Chibi_url
from chibi_dl.site.base.exceptions import Max_retries_reach


from chibi_dl.site.base.site import Site


logger = logging.getLogger( "chibi_dl.sites.tmo_fans.episode" )


class Episode( Site ):
    def download( self, path ):
        logger.info(
            "iniciando la descarga de las {} imagenes del capitulo {}".format(
                len( self.images_urls ), self.number,
            ) )
        for image_name, url in self.enumerate_images_urls():
            referer = self.url + '/'
            image = self.get(
                url=url, headers={ 'Referer': str( referer ) },
                ignore_status_code=[ 403 ] )
            if not image.ok:
                logger.warning( "no se encontro una imagen" )
                continue
            full_path = path + image_name
            f = full_path.open()
            logger.debug( "descargando {}".format( url ) )
            f.write( image.content )
            logger.debug( f"imagen {f} guardada" )

    def compress( self, path_ouput, path_input, format="zip" ):
        logger.info( "comprimiendo capitulo usando {}".format( format ) )
        file_name = str( path_ouput + self.number )
        result = Chibi_path( shutil.make_archive(
            file_name, format, str( path_input ) ) )
        expected = result.replace_extensions( "cbz" )
        result.move( expected )
        return expected

    @property
    def file_name( self ):
        return "{}.{}".format( self.number, "cbz" )

    @property
    def number( self ):
        re_float = re.compile( r"[-+]?([0-9]*\.[0-9]+|[0-9]+)" )
        return re_float.findall( self.title )[0]

    @property
    def images_urls( self ):
        try:
            return self._images_urls
        except AttributeError:
            self.load_soup()
            return self._images_urls

    def load_soup( self, delay=0, retries=0, max_retries=5, ):
        if retries > max_retries:
            logger.exception( "maximo numero de reintentos para {url}" )
            raise Max_retries_reach( self, url )
        if delay > 0:
            time.sleep( delay )

        page = self.get(
            url=self.url, headers={ "Referer": str( self.parent.url ) } )
        page_soup = BeautifulSoup( page.content, 'html.parser' )
        first_link = page_soup.select_one( 'a' ).get( 'href' )
        if first_link != 'https://lectortmo.com':
            logger.info(
                f'load_soup el primer link no tiene '
                f'la pagina de tmo {first_link}' )
            parts = Chibi_url( page._response.url ).path.rsplit( '/', 2 )[-2:]
            url = Chibi_url( 'https://lectortmo.com/viewer' ) + parts[0]
            url = url + 'cascade'
            logger.info( f"contrullendo la url {url}" )
            self.load_soup_cascade( url )
            return

        if 'cascade' not in page._response.url:
            cascade_url = page_soup.select_one(
                'a.nav-link[title="Cascada"]' ).get( 'href' )
        else:
            cascade_url = page._response.url
        self.load_soup_cascade( cascade_url )

    def load_soup_cascade( self, url, delay=0, retries=0, max_retries=5, ):
        if retries > max_retries:
            logger.exception( "maximo numero de reintentos para {url}" )
            raise Max_retries_reach( self, url )
        if delay > 0:
            time.sleep( delay )

        cascade = self.get( url=url )
        soup = BeautifulSoup( cascade.content, 'html.parser' )

        first_link = soup.select_one( 'a' ).get( 'href' )
        if first_link != 'https://lectortmo.com':
            logger.info(
                f'load_soup_cascade el primer link no tiene '
                f'la pagina de tmo {first_link}' )
            parts = Chibi_url(
                cascade._response.url ).path.rsplit( '/', 2 )[-2:]
            url = Chibi_url( 'https://lectortmo.com/viewer' ) + parts[0]
            url = url + 'cascade'
            logger.info( f"contrullendo la url {url}" )
            self.load_soup_cascade( url  )
            return
            self.load_soup( delay=10, retries=retries + 1 )
        container = soup.find(
            "div", { "class", "viewer-container container" } )
        if not container:
            self.load_soup( url, delay=10, retries=retries + 1 )
        images = container.find_all( "img" )
        self._images_urls = [ img.get( "data-src" ) for img in images ]

    def enumerate_images_urls( self ):
        for i, url in enumerate( self.images_urls ):
            ext = url.rsplit( '.', 1 )[-1]
            yield "{}.{}".format( i, ext ), url
