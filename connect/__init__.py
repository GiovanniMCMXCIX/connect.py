# -*- coding: utf-8 -*-

"""
Connect API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Monstercat Connect API.

:copyright: (c) 2016-2017 GiovanniMCMXCIX
:license: MIT, see LICENSE for more details.
"""

__title__ = 'connect'
__author__ = 'GiovanniMCMXCIX'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016-2017 GiovanniMCMXCIX'
__version__ = '0.2.0'

from .errors import *
from .client import Client
from .release import Release
from .track import Track
from .artist import Artist
from .playlist import Playlist
from . import utils
from collections import namedtuple

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=2, micro=0, releaselevel='final', serial=0)
