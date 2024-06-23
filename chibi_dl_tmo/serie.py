import copy
import itertools
import logging
import time

from bs4 import BeautifulSoup
from chibi.file.temp import Chibi_temp_path
from chibi.atlas import Chibi_atlas

from .episode import Episode
from chibi_dl_tmo.site import TMO_fans as Site


logger = logging.getLogger( "chibi_dl.sites.tmo_fans.serie" )


class Serie( Site ):
    def download( self, path, amount=None ):
        serie_path = ( path + self.name ).made_safe()
        serie_path.mkdir()

        meta = serie_path + "metadata.yml"
        meta.open().write( self.metadata )
        basura, ext = self.cover_url.base_name.rsplit( '.', 1 )
        self.cover_url.download( serie_path + f'cover.{ext}' )

        logger.info( "iniciando descarga de la serie '{}' de {}".format(
            self.name, self.url ) )
        if amount:
            episodes = itertools.islice( self.episodes, amount )
        else:
            episodes = self.episodes
        for episode in episodes:
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
                print( e )
                #import pdb
                #pdb.post_mortem( e.__traceback__ )
                #import pdb
                #pdb.set_trace()
                continue
            path_episode = episode.compress( serie_path, downlaod_folder )
            logger.info( f"episodio descargado '{path_episode}'" )
            logger.info(
                'termino de descargar el capitulo esperando '
                '10 segundos' )
            time.sleep( 10 )
        logger.info(
            'termino de descargar los episodios esperando '
            '5 segundos' )
        time.sleep( 5 )

    @property
    def name( self ):
        return self.info.title

    @property
    def episodes( self ):
        return self.info.episodes

    @property
    def cover_url( self ):
        img = self.soup.select( "section" )[1].select_one( "img" )
        return self.build_url( img.get( 'src' ) )

    def parse_metadata( self ):
        meta = copy.copy( self.info )
        meta.url = str( self.url )
        meta.pop( 'episodes' )
        return meta

    def parse_info( self ):
        result = Chibi_atlas()
        try:
            result.title = "".join(
                self.soup.select( ".element-title.my-2" )[0].find_all(
                    text=True, recursive=False ) ).strip()
            result.episodes = self.load_episodes( self.soup )
            data = self.soup.select( "section" )[1]
            result.tags = list( c.text.lower() for c in data.select( "h6" ) )
            result.other_titles = list(
                c.text.lower() for c in data.select( "span.badge" ) )
            result.synopsis = data.select_one( 'p.element-description' ).text

            staff = self.soup.select( "div.card-body" )
            result.staff = []
            for s in staff:
                rol = s.b.text
                name = s.h5.text
                name = name.replace( ',', '' ).strip()
                result.staff.append( dict( rol=rol, name=name ) )
        except Exception as e:
            print( e )
            import pdb
            pdb.post_mortem( e.__traceback__ )
            import pdb
            pdb.set_trace()
            raise
        return result

    def load_episodes( self, soup ):
        episodes = []
        if "one_shot" in self.url:
            return self.load_one_shot( soup )
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

                episodes.append(
                    Episode.from_site(
                        site=self, url=url, fansub=fansub, title=title ) )
        return episodes

    def load_one_shot( self, soup ):
        episodes = []
        chapters = soup.find( "div", { "class": "card chapter-list-element" } )
        chapters = chapters.ul.find_all( "li", recursive=False )
        for i, chapter in enumerate( chapters ):
            parts = chapter.div.find_all( "div", recursive=False )
            url = parts[-1].a.get( "href" ).strip()

            episodes.append(
                Episode.from_site(
                    site=self, url=url, fansub=parts[0].text.strip(),
                    title=str( i ) ) )
        return episodes
