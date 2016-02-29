from os import path
from setuptools import setup, find_packages


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='RestUnlClient',
    description='UNetLab REST Client Library',
    author='Michael Kashin',
    long_description=read('README'),
    version='0.1.1',
    packages=find_packages(exclude=['tests']),
    keywords='unetlab rest api sdk library client',
    license='MIT',
    url='https://github.com/networkop/rest-blog-unl-client.git',
    install_requires=['requests'],
)
