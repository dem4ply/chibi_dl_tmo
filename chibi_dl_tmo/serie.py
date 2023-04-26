import itertools
import logging
import time

from bs4 import BeautifulSoup
from chibi.file.temp import Chibi_temp_path

from .episode import Episode
from chibi_dl.site.base.site import Site


logger = logging.getLogger( "chibi_dl.sites.tmo_fans.serie" )


class Serie( Site ):
    def __init__( self, url, *args, **kw ):
        super().__init__( url, *args, **kw )

    def download( self, path ):
        serie_path = ( path + self.name ).made_safe()
        serie_path.mkdir()

        logger.info( "iniciando descarga de la serie '{}' de {}".format(
            self.name, self.url ) )
        for episode in self.episodes:
            episode_path = serie_path + episode.file_name
            if ( episode_path.exists ):
                logger.info( (
                    "ignorando el episodio {} se encontro "
                    "en el destino" ).format( episode.title ) )
                continue
            downlaod_folder = Chibi_temp_path()
            try:
                episode.download( downlaod_folder )
            except Exception as e:
                logger.exception(
                    "paso un problema cuando intento de "
                    "descargar el episodio" )
                continue
            episode.compress( serie_path, downlaod_folder )
            logger.info(
                'termino de descargar el episodio esperando '
                '10 seguncods para el siguiente' )
            time.sleep( 10 )

    @property
    def name( self ):
        try:
            return self._title
        except AttributeError:
            self.load_soup()
            return self._title

    @property
    def episodes( self ):
        try:
            return self._episodes
        except AttributeError:
            self.load_soup()
            return self._episodes

    def load_soup( self ):
        page = self.get( self.url, )
        soup = BeautifulSoup( page.content, 'html.parser' )
        try:
            self._title = "".join(
                soup.select( ".element-title.my-2" )[0].find_all(
                    text=True, recursive=False ) ).strip()
            self.load_episodes( soup )
        except Exception as e:
            import pdb
            pdb.post_mortem( e.__traceback__ )
            raise

    def load_episodes( self, soup ):
        self._episodes = []
        if "one_shot" in self.url:
            self.load_one_shot( soup )
            return
        else:
            chapter_container = soup.find(
                "div", { 'class': "card chapters" } )
            chapter_container_hidden = chapter_container.find(
                "div", id="chapters-collapsed" )

            if not chapter_container_hidden:
                chapters = chapter_container.ul.find_all(
                    "li", recursive=False )
            else:
                chapters = itertools.chain(
                    chapter_container.ul.find_all( "li", recursive=False ),
                    chapter_container_hidden.find_all( "li", recursive=False )
                )

            for chapter in chapters:
                links = chapter.select(
                    "div.card.chapter-list-element" )[0].find_all( 'a' )
                fansub = links[0].text
                title = chapter.find( "h4" ).a.text
                url = links[0].find_next(
                    "span", { "class": "fas fa-play fa-2x"}
                ).parent.get( 'href' )

                self._episodes.append(
                    Episode.from_site(
                        site=self, url=url, fansub=fansub, title=title ) )

    def load_one_shot( self, soup ):
        chapters = soup.find( "div", { "class": "card chapter-list-element" } )
        chapters = chapters.ul.find_all( "li", recursive=False )
        for i, chapter in enumerate( chapters ):
            parts = chapter.div.find_all( "div", recursive=False )
            url = parts[-1].a.get( "href" ).strip()

            self._episodes.append(
                Episode.from_site(
                    site=self, url=url, fansub=parts[0].text.strip(),
                    title=str( i ) ) )
