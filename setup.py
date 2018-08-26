# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="mpl_finance_ext",
    version="0.1.0",
    author="z33pX",
    author_email="z33px.contact@gmail.com",
    description="This package provides some compact functions for evaluating finance data. "
                "It is build on top of matplotlib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/z33pX/mpl_finance_ext",
    packages=find_packages(),
    license=license
)