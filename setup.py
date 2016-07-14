#!/usr/bin/env python
import ipfsApi
import os, sys
from pprint import pprint
from requests.exceptions import ConnectionError
from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py as _build_py


reqs_file = os.path.join(os.path.dirname(os.path.realpath(__file__))
                   , "requirements.txt")

reqs = None
with open(reqs_file) as f:
    reqs = f.readlines()

class ChDir(object):
    """
    Step into a directory temporarily
    """
    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path
 
    def __enter__(self):
        os.chdir(self.new_dir)
 
    def __exit__(self, *args):
        os.chdir(self.old_dir)

class PublishTranslators(Command):
    user_options = []

    def initialize_options(self):
        """N/A"""

    def finalize_options(self):
        """N/A"""

    def run(self):
        print(" => IPFS READY!")
        host = "localhost"
        port = 5001
        self.client = ipfsApi.Client(host, port)
        try:
            self.client.id()
        except ConnectionError:
            raise Exception(
                'Unable to connect to ipfs API at {}:{} \n'
                'For ipfs installation instructions see '
                'https://ipfs.io/docs/install'.format(host, port)
            )
        res = {}
        with ChDir('translators'):
            for translator in os.listdir('.'):
                print "adding " + translator
                res[translator] = self.client.add(translator)['Hash']
        pprint(res)


setup(
    version='0.1.2',
    name='mediachain-schema-translators',
    description='collection of mediachain schema translator modules',
    author='Mediachain Labs',
    packages=find_packages('.'),
    author_email = 'hello@mediachainlabs.com',
    url='http://mediachain.io',
    install_requires=reqs,
    cmdclass={'publish_translators': PublishTranslators},
    setup_requires=['pytest-runner>=2.8', 'ipfs-api==0.2.3' ],
    tests_require=['pytest>=2.9.2'],
)
