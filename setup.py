import os
from setuptools import setup

setup(
    entry_points={
        "console_scripts": [
            "qcaide = qcaide.qcaide:main",
        ]
    }
)
