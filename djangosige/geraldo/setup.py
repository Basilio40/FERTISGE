# Geraldo setup

# Downloads setuptools if not find it before try to import
try:
    from setuptools import setup, find_packages
except:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools import setup
from djangosige.geraldo.geraldo.version import __version__

setup(
    name = 'Geraldo',
    version = __version__,
    description = 'Geraldo is a reports engine for Python and Django applications',
    long_description = 'Geraldo is a Python and Django pluggable application that works with ReportLab to generate complex reports.',
    author = 'Marinho Brandao',
    author_email = 'marinho@gmail.com',
    url = 'http://www.geraldoreports.org/',
    #download_url = 'http://ufpr.dl.sourceforge.net/sourceforge/geraldo/Geraldo-0.2-stable.tar.gz',
    license = 'GNU Lesser General Public License (LGPL)',
    packages = ['geraldo', 'geraldo.tests', 'geraldo.generators',],
    install_requires = ['reportlab', 'six',],
)
