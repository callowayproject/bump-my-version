"""Tests for the bumpversion.click_config module."""

from pathlib import Path

import click
import httpx
import pytest

from bumpversion.click_config import config_option, resolve_conf_location, download_url
from bumpversion.exceptions import BadInputError


@click.command()
@config_option()
def hello(config: Path):
    """Say hello."""
    click.echo(f"Hello {config}!")
    click.echo(f"path exists: {config.exists()}")


class TestConfigOption:
    """Tests to for config_option."""

    def test_config_option(self, runner):
        """Passing an invalid option should raise an error."""
        result = runner.invoke(hello, ["--config", "idont/exist.txt"])

        assert result.exit_code == 0
        assert "path exists: False" in result.output


class TestResolveConfLocation:
    """Tests for resolve_conf_location."""

    def test_resolves_file_path(self, fixtures_path: Path):
        """Should return a Path object for a valid local file path."""
        dummy_path = fixtures_path / "basic_cfg.toml"
        result = resolve_conf_location(str(dummy_path))
        assert isinstance(result, Path)
        assert result == dummy_path

    def test_resolves_valid_url(self, mocker):
        """Should download the file if given a valid URL."""
        # Arrange
        mocked_download = mocker.patch(
            "bumpversion.click_config.download_url", return_value=Path("/tmp/downloaded_config.txt")
        )
        url = "http://example.com/config.txt"

        # Act
        result = resolve_conf_location(url)

        # Assert
        mocked_download.assert_called_once_with(url)
        assert isinstance(result, Path)
        assert str(result) == "/tmp/downloaded_config.txt"


class TestDownloadUrl:
    """Tests for download_url."""

    def test_download_url_success(self, mocker, tmp_path: Path):
        """Should return a Path for a valid request."""
        # Arrange
        mock_response = mocker.Mock(spec=httpx.Response)
        mock_response.status_code = 200
        mock_response.text = "content"
        mocker.patch("httpx.get", return_value=mock_response)
        tmp_file = tmp_path / "tempfile.txt"
        mock_tempfile = mocker.patch("bumpversion.click_config.NamedTemporaryFile", autospec=True)
        temp_file_instance = mock_tempfile.return_value.__enter__.return_value
        temp_file_instance.name = str(tmp_file)

        # Act
        result = download_url("http://example.com/config.txt")

        # Assert
        assert isinstance(result, Path)
        assert result == tmp_file
        mock_tempfile.assert_called_once()

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
