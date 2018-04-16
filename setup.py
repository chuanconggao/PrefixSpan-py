#! /usr/bin/env python3

from setuptools import setup

setup(
    name="prefixspan",
    packages=["prefixspan"],
    scripts=["prefixspan-cli"],
    version="0.2",
    description="PrefixSpan in Python 3",
    author="Chuancong Gao",
    author_email="chuancong@gmail.com",
    url="https://github.com/chuanconggao/PrefixSpan-py",
    download_url="https://github.com/chuanconggao/PrefixSpan-py/tarball/0.2",
    keywords=[
        "data mining",
        "pattern mining"
    ],
    license="MIT",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">= 3",
    install_requires=[
        "docopt >= 0.6.2",
    ]
)
