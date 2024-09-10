from pathlib import Path
import tempfile

from qcaide import Submission
from qcaide.qcaide import readme_tmpl


def test_load_td():
    Submission.from_toml("qcaide/_tests/data/td.toml")


def test_default():
    s = Submission.default()
    with tempfile.NamedTemporaryFile("w") as f:
        print(s, file=f, flush=True)
        Submission.from_toml(f.name)


def test_readme_template():
    sub = Submission.from_toml("qcaide/_tests/data/td.toml")
    got = readme_tmpl.render(sub=sub, date="today")
    want = Path("qcaide/_tests/data/td.want").read_text()

    assert got == want
