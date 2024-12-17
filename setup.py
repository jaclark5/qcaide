import os
from setuptools import setup

filename = "qcaide/dat/qca_dataset_submission_path"
if not os.path.isfile(filename):
    file = open(filename, "w")
    file.write("EXECPATHHERE")
    file.close()

setup(
    entry_points={
        "console_scripts": [
            "qcaide = qcaide.qcaide:main",
        ]
    }
)
