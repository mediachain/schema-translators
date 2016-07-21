#!/usr/bin/env python
import distutils.spawn
import os, sys
from pprint import pprint
from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py as _build_py
import subprocess


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


    def add(self, path):
        """
        we'd prefer to use ipfsApi like this:
        return self.client.add(t, True)['Hash']
        but see https://github.com/ipfs/py-ipfs-api/issues/45
        """
        if not distutils.spawn.find_executable('ipfs'):
            raise Exception(
                'Unable to find ipfs executable'
                'For ipfs installation instructions see '
                'https://ipfs.io/docs/install'.format(host, port)
            )
        out = subprocess.check_output(["ipfs", "add", "-r", path])
        return out.strip().split('\n')[-1].split(' ')[1]



    def run(self):
        print("Publishing to IPFS!")
        with ChDir('mediachain/translation'):
            res = {t: self.add(t) for t in os.listdir('.') if not t.startswith('_')}
        pprint(res)


setup(
    version='0.1.2',
    name='mediachain-schema-translators',
    description='collection of mediachain schema translator modules',
    author='Mediachain Labs',
    packages=find_packages('.'),
    author_email = 'hello@mediachainlabs.com',
    url='http://mediachain.io',
    install_requires=['mediachain-client>=0.1.4'],
    cmdclass={'publish_translators': PublishTranslators},
    setup_requires=['pytest-runner>=2.8'],
    tests_require=['pytest>=2.9.2'],
)

