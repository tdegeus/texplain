
from setuptools import setup
from setuptools import find_packages
import re

filepath = 'texplain/__init__.py'
__version__ = re.findall(r'__version__ = \'(.*)\'', open(filepath).read())[0]

setup(
    name = 'texplain',
    version = __version__,
    license = 'MIT',
    author = 'Tom de Geus',
    author_email = 'tom@geus.me',
    description = 'Create directory with TeX-file and only dependencies.',
    long_description = 'Create directory with TeX-file and only dependencies.',
    keywords = 'LaTeX',
    url = 'https://github.com/tdegeus/texplain',
    packages = find_packages(),
    install_requires = ['docopt>=0.6.2', 'click>=4.0', 'numpy>=0.0.1'],
    entry_points = {'console_scripts': ['texplain = texplain:main']})
