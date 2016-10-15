"""
Connect API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Monstercat Connect API.
:copyright: (c) 2016 GiovanniMCMXCIX
:license: MIT, see LICENSE for more details.
"""

from .client import Client
from .download import Download
from .search import SearchSimple, SearchAdvanced
from .get import Get, DownloadLink
from .load import Load

__title__ = 'connect'
__author__ = 'GiovanniMCMXCIX'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 GiovanniMCMXCIX'
__version__ = '0.1'
__all__ = ["Client", "Download", "DownloadLink", "SearchSimple", "SearchAdvanced", "Get", "Load"]
