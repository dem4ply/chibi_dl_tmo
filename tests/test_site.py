#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase, skip
from chibi.file import Chibi_path
from vcr_unittest import VCRTestCase
from chibi.file.temp import Chibi_temp_path
from chibi_dl_tmo.site import TMO_fans
from vcr.record_mode import RecordMode
import logging


class Test_tmofans:
    def _get_vcr_kwargs( self, **kw ):
        result = super()._get_vcr_kwargs( **kw )
        result[ 'ignore_localhost' ] = True
        result[ 'ignore_hosts' ] = [
            'chromedriver.storage.googleapis.com',
        ]
        #result[ 'record_mode' ] = RecordMode.NEW_EPISODES
        return result

    def test_the_series_should_find_his_own_name( self ):
        self.assertIsInstance( self.site.series[0].name, str )

    def test_have_a_list_of_episodes( self ):
        self.assertTrue( self.site.series[0].episodes )
        for episode in self.site.series[0].episodes:
            self.assertTrue( episode.title )
            self.assertTrue( episode.fansub )
            self.assertTrue( episode.url )
            self.assertIsInstance( float( episode.number ), float )

    def test_the_episode_should_have_a_list_of_images( self ):
        episode = self.site.series[0].episodes[0]
        self.assertTrue( episode.images_urls )

    def test_should_download_the_images_in_a_folder( self ):
        folder = Chibi_temp_path()
        episode = self.site.series[0].episodes[0]
        episode.download( folder )
        self.assertTrue( next( folder.ls() ) )
        for f in folder.ls():
            properties = f.open().properties
            self.assertGreater( properties.size, 1024 )

    @skip( 'esta mierda es muy lenta' )
    def test_should_can_compress_the_download_files( self ):
        folder = Chibi_temp_path()
        folder_compress = Chibi_temp_path()
        episode = self.site.series[0].episodes[0]
        episode.download( folder )
        result = episode.compress( folder_compress, folder )
        self.assertIsInstance( result, Chibi_path )
        self.assertTrue( result.exists )
        self.assertTrue( result.endswith( ".cbz" ) )
        self.assertIn( result, folder_compress )

    @skip( 'esta mierda es muy lenta' )
    def test_should_donwload_all_the_serie( self ):
        folder = Chibi_temp_path()
        serie = self.site.series[0]
        serie.download( folder )
        download_files = list( next( folder.ls() ).ls() )
        self.assertEqual( len( serie.episodes ), len( download_files ) )


@skip( "quitaron el link" )
class Test_spy_family( Test_tmofans, VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.site = TMO_fans()
        self.site.append(
            'https://lectortmo.com/library/manga/43882/spy-x-family' )

    def test_serie_should_be_the_url_of_the_spy_x_family( self ):
        self.assertEqual(
            self.site.series[0].url,
            'https://lectortmo.com/library/manga/43882/spy-x-family' )


class Test_king_from_hell( Test_tmofans, VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.site = TMO_fans()
        self.site.append(
            'https://visortmo.com/library/manga/79656/king-from-hell' )

    def test_serie_should_be_the_url_of_the_spy_x_family( self ):
        self.assertEqual(
            self.site.series[0].url,
            'https://visortmo.com/library/manga/79656/king-from-hell' )


class Test_tmp_basic( TestCase ):
    def setUp( self ):
        super().setUp()
        self.site = TMO_fans()

    def test_on_init_should_not_have_browser( self ):
        self.assertFalse( self.site._has_browser_init )

    def test_should_no_open_the_browser_when_do_the_append( self ):
        self.assertFalse( self.site.is_browser_open )
        self.site.append( 'https://lectortmo.com/' )
        self.assertFalse( self.site.is_browser_open )
