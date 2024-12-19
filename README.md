# qcaide
Helper for generating [qca-dataset-submission][qca] submissions


## Installation

Install `qcaide` into your current virtual environment with:

``` shell
pip install -e .
```

### Dependencies

`qcaide` makes use of the `tomllib` module in Python 3.11, so you'll need at
least that version of Python. The only external dependency is [jinja][jinja],
which is very likely to be installed already in your
[qca-dataset-submission][qca] environment.

## Usage

You can generate an empty input TOML file with the `default` subcommand:

``` shell
python -m qcaide default
```

This prints to stdout, so you'll likely want to direct the output into a file,
which will look something like the example below, but without any of the filled
data fields. Note that the comments will not be present when run.

``` toml
name = "OpenFF Sage 2.0.0 Torsion Drive Training Dataset v1.0"
description = ""
short_description = "B3LYP-D3BJ/DZVP conformers applicable to drug-like molecules for OpenFF 2.0.0 Sage"
class = ""   # Either optimization or torsiondrive
purpose = "Complete set of training data for OpenFF 2.0.0 Sage"
submitter = "" # The person submitting this dataset, you!
generator = "" # The person that ran and curated the data

[[pipeline]]
filename = "generate-combined-dataset.py"
description = "A python script which shows how the dataset was prepared from the input files."

[[manifest]]
filename = "generate-combined-dataset.py"

[[manifest]]
filename = "dataset.json.bz2"
description = "The basic dataset ready for submission."

[[manifest]]
filename = "dataset.pdf"
description = "A pdf file containing molecule 2D structures."

[[manifest]]
filename = "dataset.smi"
description = "SMILES for every molecule in the submission."
```

Once you populate the TOML file, you can generate a new QCA submission with the
`create` subcommand in the root of your qca-dataset-submission repo:

``` shell
python -m qcaide create input.toml
```

This will create the directory `submissions/DATE-Your-Submission-Name`, where
`DATE` will be today's date, and `Your-Submission-Name` is taken from the `name`
field in your input file. This also generates a README template for your
submission, populating it with the other values from the input file.

Finally, you can generate most of the main README file table entry for your
dataset with the `readme` subcommand:

``` shell
python -m qcaide readme input.toml
```

As long as the current date is the same as the day you generated the submission,
this will emit a Markdown table line that you can paste into the appropriate
table in the main README. Just remember to add the elements field in the
second-to-last column.

[jinja]: https://jinja.palletsprojects.com/en/3.1.x/
[qca]: https://github.com/openforcefield/qca-dataset-submission
