# -*- coding: utf-8 -*-
from chibi.config import configuration, basic_config


basic_config()

configuration.loggers[ 'vcr.stub' ].level = 'INFO'
#configuration.loggers[ 'vcr.cassette' ].level = 'WARNING'
configuration.loggers[ 'vcr' ].level = 'WARNING'
