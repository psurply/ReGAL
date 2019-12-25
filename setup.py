#! /usr/bin/env python3

import sys
from setuptools import setup
from setuptools import find_packages


setup(
    name="regal",
    version="0.1",
    author="Pierre Surply",
    author_email="pierre.surply@lse.epita.fr",
    install_requires=[
        "pyserial",
        "quine_mccluskey",
        "pyyaml"
    ],
    packages=find_packages(),
    package_data={
        "regal.synth": ["*.v"]
    },
    entry_points={
          "console_scripts": [
              "regal = regal.__main__:main"
          ]
    },
    include_package_data=True,
    license="MIT",
    platforms=["Any"]
)
