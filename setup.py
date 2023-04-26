from setuptools import setup

setup(
    name='sentinoapi',
    version='0.1.0',
    description='A Python API wrapper for the Sentino API',
    author='Andrew Ryder',
    author_email='andrewtryder@gmail.com',
    url='https://github.com/andrewtryder/sentino-api-wrapper',
    packages=['sentinoapi'],
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='sentino api wrapper',
)
