#!/usr/bin/env python

import argparse
import json
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from jinja2 import BaseLoader, Environment

readme_tmpl = """\
# {{sub.name}}

## Description

{{sub.description}}

## General Information

* Date: {{date}}
* Class: {{sub.class_}}
* Purpose: {{sub.purpose}}
* Name: {{sub.name}}
* Number of unique molecules: {{num_uniq}}
* Number of filtered molecules: {{num_filt}}
* Number of conformers: {{num_conf}}
* Number of conformers per molecule (min, mean, max): {{conf_min}}, \
{{conf_mean}}, {{conf_max}}
* Mean molecular weight: {{mean_weight}}
* Max molecular weight: {{max_weight}}
* Charges: {{charges}}
* Dataset submitter: {{sub.submitter}}
* Dataset generator: {{sub.generator}}

## QCSubmit Generation Pipeline

{% for p in sub.pipeline %}
{%- if p.filename -%}
* `{{p.filename}}`: {{p.description}}
{% else -%}
* {{p.description}}
{%- endif -%}
{%- endfor %}

## QCSubmit Manifest

{% for p in sub.manifest -%}
* `{{p.filename}}`: {{p.description}}
{% endfor %}
## Metadata

* elements: {{elements}}
* Spec: {{spec}}
"""

readme_tmpl = Environment(loader=BaseLoader()).from_string(readme_tmpl)

torsion_drive_line = (
    "| `{{name}}` | [{{date_name}}]"
    "(https://github.com/openforcefield/qca-dataset-submission/tree/master/"
    "submissions/{{date_name}}) | {{short_description}} | | |"
)
torsion_drive_line = Environment(loader=BaseLoader()).from_string(
    torsion_drive_line
)


@dataclass
class Pipeline:
    description: str
    filename: str | None = None

    def __post_init__(self):
        self.description = self.description.strip()


@dataclass
class Manifest:
    description: str
    filename: str

    def __post_init__(self):
        self.description = self.description.strip()


class Submission:
    name: str
    description: str
    short_description: str
    class_: str  # alias class from toml, enum of optimization | torsiondrive
    purpose: str
    submitter: str
    generator: str | None  # defaults to submitter if omitted
    pipeline: list[Pipeline]
    manifest: list[Manifest]

    def __init__(self):
        pass

    @classmethod
    def default(cls):
        self = cls()

        self.name = ""
        self.description = ""
        self.short_description = ""
        self.class_ = ""
        self.purpose = ""
        self.submitter = ""
        self.generator = ""
        self.pipeline = ""
        self.manifest = [Manifest("", "")]

        return self

    @classmethod
    def from_toml(cls, filename):
        self = cls()
        with open(filename, "rb") as f:
            data = tomllib.load(f)
        self.name = data["name"].strip()
        self.description = data["description"].strip()
        self.short_description = data["short_description"].strip()
        match data["class"]:
            case "torsiondrive":
                self.class_ = "OpenFF TorsionDrive Dataset"
            case "optimization":
                self.class_ = "OpenFF Optimization Dataset"
            case misc:
                print(
                    f"warning: unrecognized dataset class: {misc}",
                    file=sys.stderr,
                )
        self.purpose = data["purpose"].strip()
        self.submitter = data["submitter"].strip()

        if gen := data.get("generator", None):
            self.generator = gen
        else:
            self.generator = self.submitter

        self.pipeline = [Pipeline(**p) for p in data["pipeline"]]
        self.manifest = [Manifest(**d) for d in data["manifest"]]

        return self


@dataclass
class Metadata:
    num_uniq: int
    num_filt: int
    num_conf: int
    conf_min: int
    conf_mean: float
    conf_max: int
    mean_weight: float
    max_weight: float
    charges: set[int]
    elements: set[str]
    spec: dict[str, str]

    @classmethod
    def from_json(cls, filename):
        with open(filename) as f:
            data = json.load(f)
        return cls(**data)


def create(args):
    sub = Submission.from_toml(args.input_file)
    submissions = Path("submissions/")
    date = datetime.today().strftime("%Y-%m-%d")
    base = "-".join(sub.name.split())
    date_name = f"{date}-{base}"
    dir_ = submissions / date_name
    print(f"creating {dir_}")
    dir_.mkdir(exist_ok=True)
    readme = Path(dir_ / "README.md")
    if readme.exists():
        exit(0)
    with open(readme, "w") as out:
        print(readme_tmpl.render(sub=sub, date=date), file=out)


def readme(args):
    sub = Submission.from_toml(args.input_file)
    date = datetime.today().strftime("%Y-%m-%d")
    base = "-".join(sub.name.split())
    date_name = f"{date}-{base}"
    print(
        torsion_drive_line.render(
            name=sub.name,
            date_name=date_name,
            short_description=sub.short_description,
        )
    )


def main():
    parser = argparse.ArgumentParser(prog="qcaide")
    subparsers = parser.add_subparsers(required=True, help="sub-command help")

    create_p = subparsers.add_parser("create")
    create_p.add_argument("input_file")
    create_p.set_defaults(func=create)

    readme_p = subparsers.add_parser("readme")
    readme_p.add_argument("input_file")
    readme_p.set_defaults(func=readme)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
