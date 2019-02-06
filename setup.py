try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Module for create and read special pyvoc formate.',
    'author': 'Sergey Trishkin',
    'url': 'None',
    'download_url': 'None',
    'author_email': 'grdvsng@gmail.com',
    'version': '1.0',
    'install_requires': ['nose'],
    'packages': ['pyvoc'],
    'name': 'pyvoc',
    }

setup(**config)
