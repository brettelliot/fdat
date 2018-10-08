import setuptools
import os

with open('README.rst', 'r') as fh:
    long_description = fh.read()

version_file = open(os.path.join('./', 'VERSION'))
version = version_file.read().strip()

setuptools.setup(
    name='fdat',
    version=version,
    author='Brett Elliot',
    author_email='brett@theelliots.net',
    description='A package for getting financial data like histprical stock prices.',
    long_description=long_description,
    url='https://github.com/brettelliot/fdat',
    packages=['fdat'],
    install_requires=[
        'pandas == 0.22.0',
        'requests >= 2.19.1',
        'urllib3 >= 1.23'
    ],
    license='MIT',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
