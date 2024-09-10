from qcaide import Submission
from qcaide.qcaide import readme_tmpl


def test_load_td():
    Submission.from_toml("qcaide/_tests/data/td.toml")


def test_readme_template():
    sub = Submission.from_toml("qcaide/_tests/data/td.toml")
    s = readme_tmpl.render(sub=sub, date="today")
    print(s)
    panic
