from click.testing import CliRunner, Result

from bumpversion import cli
from tests.conftest import inside_dir


def test_no_subcommand_calls_bump(mocker, tmp_path):
    """
    The legacy behavior of calling `bumpversion` with no subcommand is to call `bump`.
    """
    mocked_do_bump = mocker.patch("bumpversion.cli.do_bump")
    runner: CliRunner = CliRunner()
    with inside_dir(tmp_path):
        result: Result = runner.invoke(cli.cli, ["--current-version", "1.0.0", "--no-configured-files", "patch"])

    if result.exit_code != 0:
        print(result.output)

    assert result.exit_code == 0

    call_args = mocked_do_bump.call_args[0]
    assert len(call_args[2].files) == 0
