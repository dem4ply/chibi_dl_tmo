import logging
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import undetected_chromedriver as uc

from .exceptions import Cannot_pass_cloud_flare, Cannot_login
from .regex import re_show, re_follow, re_pending, re_read
from chibi_dl.site.base.site import Site


logger = logging.getLogger( "chibi_dl.sites.tmo_fans" )


class TMO_fans( Site ):
    def __init__( self, *args, url=None, user=None, password=None, **kw ):
        if url is None:
            url = 'https://tmofans.com/login'
        super().__init__( url, *args, **kw )
        self.series = []
        self.user = user
        self.password = password
        self._login_ok = False

    def append( self, url ):
        from .serie import Serie
        #self.cross_cloud_flare()
        if re_show.match( url ):
            self.series.append( Serie( url=url, parent=self ) )
        elif re_follow.match( url ):
            self.login()
            for l in self.get_all_follow():
                self.append( l )
        elif re_pending.match( url ):
            self.login()
            for l in self.get_all_pending():
                self.append( l )
        elif re_read.match( url ):
            self.login()
            for l in self.get_all_read():
                self.append( l )
        else:
            logger.error(
                "la url {} no se pudo identificar como serie".format( url ) )

    def cross_cloud_flare( self, delay=2 ):
        super().cross_cloud_flare( delay=delay )
        self.browser.close()

    @property
    def soup( self ):
        if not self.cloud_flare_passed:
            self.cross_cloud_flare()
        return super().soup

    def login( self ):
        if self._login_ok:
            return
        if not self.cloud_flare_passed:
            self.cross_cloud_flare()

        email = self.firefox.find_element( By.ID, "email" )
        password = self.firefox.find_element( By.ID, "password" )
        submit = self.firefox.find_element(
            By.XPATH,
            "/html/body/div[1]/main/div/div/div/div[1]/form/div[4]"
            "/div[1]/button" )

        email.send_keys( self.user )
        password.send_keys( self.password )

        submit.click()
        logger.info( "esperando 10 segundos a que termine el login" )
        time.sleep( 10 )
        if self.browser.current_url == self.url:
            raise Cannot_login
        else:
            self._login_ok = True
            self.cookies = self.firefox.get_cookies()
            self.user_agent = self.firefox.execute_script(
                "return navigator.userAgent;" )

        """
        page = self.get( self.url )
        soup = BeautifulSoup( page.content, 'html.parser' )
        form = soup.find( "form", { "class": "form-horizontal" } )
        token = form.find( "input", dict( name="_token" ) )[ "value" ]

        payload = dict(
            email=self.user, password=self.password, remember="on",
            _token=token )

        response = self.session.post(
            self.url, data=payload, headers={
                "Referer": str( self.url ),
                "Content-type": "application/x-www-form-urlencoded" } )

        if response.ok and response.url == self.url:
            raise Cannot_login
        else:
            self._login_ok = True
        """

    def get_all_follow( self ):
        page_number = 0
        url = "https://tmofans.com/profile/follow"
        while( True ):
            page_number += 1
            page = self.get( url=url, params={ "page": page_number } )
            soup = BeautifulSoup( page.content, 'html.parser' )

            links = self.get_manga_links( soup )
            if not links:
                return
            for l in links:
                yield l

    def get_all_pending( self ):
        page_number = 0
        url = "https://tmofans.com/profile/pending"
        while( True ):
            page_number += 1
            page = self.get( url=url, params={ "page": page_number } )
            soup = BeautifulSoup( page.content, 'html.parser' )

            links = self.get_manga_links( soup )
            if not links:
                return
            for l in links:
                yield l

    def get_all_read( self ):
        page_number = 0
        url = "https://tmofans.com/profile/read"
        while( True ):
            page_number += 1
            page = self.get( url=url, params={ "page": page_number } )
            soup = BeautifulSoup( page.content, 'html.parser' )

            links = self.get_manga_links( soup )
            if not links:
                return
            for l in links:
                yield l

    def get_manga_links( self, soup ):
        result = []
        for a in soup.find_all( "a" ):
            if "library/" in a[ "href" ]:
                result.append( a[ "href" ].strip() )
        return result

    def i_can_proccess_this( self, url ):
        regex = ( re_show, re_pending, re_read, re_follow )
        return any( ( r.match( url ) for r in regex ) )
