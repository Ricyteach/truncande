import pathlib
import pytest
from truncande import cli, candeout
from click.testing import CliRunner


FILE = "example.out"


@pytest.fixture
def tmp_file_path(tmpdir):
    return pathlib.Path(tmpdir.dirname)


@pytest.fixture
def cout_path():
    return pathlib.Path(FILE)


@pytest.fixture
def cout(cout_path):
    return candeout.CandeOut(cout_path.read_text().split("\n"))


@pytest.fixture
def patched_main(monkeypatch, cout):
    monkeypatch.setattr(candeout.CandeOut, "__new__", lambda s, *args, **kwargs: cout)
    return cli.main


def test_cande_out(cout, cout_path):
    assert cout.n_steps == 10
    assert cout.n_lines == 96
    assert cout.step_line_nos == list(range(7, 96, 9))
    assert "\n".join(cout.lines) == cout_path.read_text()


def test_truncande(patched_main, tmp_file_path, cout_path, cout):
    runner = CliRunner()
    result = runner.invoke(
        patched_main, [cout_path, tmp_file_path / "test.txt", "steps", "10"]
    )
    assert result.exit_code == 0
    assert len(cout.step_line_nos) == 1
