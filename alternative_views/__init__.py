"""
alternative_views
~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Linovia, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('alternative_views').version
except Exception, e:
    VERSION = 'unknown'
