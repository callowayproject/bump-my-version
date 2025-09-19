"""Tests for the bumpversion.click_config module."""

from pathlib import Path
from typing import Optional

import click
import httpx
import pytest

from bumpversion.click_config import config_option, download_url, resolve_conf_location
from bumpversion.exceptions import BadInputError


@click.command()
@config_option()
def hello(config: Optional[Path]):
    """Say hello."""
    click.echo(f"Hello {config}!")
    if config:
        click.echo(f"path exists: {config.exists()}")
    else:
        click.echo("Nothing was passed.")


class TestConfigOption:
    """Tests to for config_option."""

    def test_passing_missing_file_raises_error(self, runner):
        """Explicitly passing a path that does not exist should raise an error."""
        result = runner.invoke(hello, ["--config", "idont/exist.txt"])

        assert result.exit_code != 0

    def test_passing_nothing_returns_none(self, runner):
        """If nothing is passed, the value is `None`."""
        result = runner.invoke(hello, [])

        assert result.exit_code == 0
        assert "Hello None!" in result.output

    def test_passing_existing_file_returns_path(self, runner, fixtures_path: Path):
        """Passing an existing file path should return a Path object."""
        config_path = fixtures_path / "basic_cfg.toml"
        result = runner.invoke(hello, ["--config", str(config_path)])

        assert result.exit_code == 0
        assert f"Hello {config_path}!" in result.output

    def test_passing_url_returns_path(self, runner, fixtures_path: Path, httpserver):
        """Passing an existing file path should return a Path object."""
        # Assemble
        config = fixtures_path.joinpath("basic_cfg.toml").read_text()
        httpserver.serve_content(config)

        # Act
        result = runner.invoke(hello, ["--config", f"{httpserver.url}/basic_cfg.toml"])

        # Assert
        assert result.exit_code == 0
        assert "path exists: True" in result.output


class TestResolveConfLocation:
    """Tests for resolve_conf_location."""

    def test_resolves_file_path(self, fixtures_path: Path):
        """Should return a Path object for a valid local file path."""
        dummy_path = fixtures_path / "basic_cfg.toml"
        result = resolve_conf_location(str(dummy_path))
        assert isinstance(result, Path)
        assert result == dummy_path

    def test_resolves_valid_url(self, fixtures_path: Path, httpserver):
        """Should download the file if given a valid URL."""
        # Arrange
        config = fixtures_path.joinpath("basic_cfg.toml").read_text()
        httpserver.serve_content(config)
        url = f"{httpserver.url}/basic_cfg.toml"

        # Act
        result = resolve_conf_location(url)

        # Assert
        assert isinstance(result, Path)
        assert result.read_text() == config


class TestDownloadUrl:
    """Tests for download_url."""

    def test_download_url_success(self, fixtures_path: Path, httpserver):
        """Should return a Path for a valid request."""
        # Arrange
        config = fixtures_path.joinpath("basic_cfg.toml").read_text()
        httpserver.serve_content(config)
        url = f"{httpserver.url}/basic_cfg.toml"

        # Act
        result = download_url(url)

        # Assert
        assert isinstance(result, Path)
        assert result.read_text() == config

    def test_download_url_request_error(self, mocker):
        """Should raise BadInputError for a RequestError."""
        # Arrange
        mocker.patch("httpx.get", side_effect=httpx.RequestError("Request failed"))

        # Act & Assert
        with pytest.raises(BadInputError, match="Unable to download configuration from URL"):
            download_url("http://example.com/config.txt")

    def test_download_url_http_status_error(self, mocker):
        """Should raise BadInputError for an HTTPStatusError."""
        mock_response = mocker.Mock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Error", request=mocker.Mock(), response=mock_response
        )
        mocker.patch("httpx.get", return_value=mock_response)

        # Act & Assert
        with pytest.raises(BadInputError, match="Error response 404 while requesting"):
            download_url("http://example.com/config.txt")
