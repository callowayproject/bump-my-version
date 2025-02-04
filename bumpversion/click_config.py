"""A configuration option for click."""

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Optional, Sequence, Union
from urllib.parse import urlparse

import httpx
from click import Context, Option
from click.decorators import FC, _param_memo  # noqa: PLC2701

from bumpversion.exceptions import BadInputError, BumpVersionError
from bumpversion.ui import get_indented_logger

logger = get_indented_logger(__name__)

BoolOrStr = Union[bool, str]
StrSequence = Sequence[str]


class ConfigOption(Option):
    """A configuration option for click."""

    def __init__(
        self,
        param_decls: Optional[StrSequence] = None,
        show_default: Optional[BoolOrStr] = None,
        allow_from_autoenv: bool = True,
        help: Optional[str] = None,
        show_envvar: bool = False,
        **attrs,
    ):
        param_decls = param_decls or ("--config", "-C")
        multiple = False
        count = False
        hidden = False
        show_choices = True
        prompt = False
        confirmation_prompt = False
        is_flag = None
        flag_value = None
        prompt_required = True
        hide_input = False
        type_ = str
        meta_var = "PATH_OR_URL"

        super().__init__(
            param_decls=param_decls,
            show_default=show_default,
            prompt=prompt,
            confirmation_prompt=confirmation_prompt,
            prompt_required=prompt_required,
            hide_input=hide_input,
            is_flag=is_flag,
            flag_value=flag_value,
            metavar=meta_var,
            multiple=multiple,
            count=count,
            allow_from_autoenv=allow_from_autoenv,
            type=type_,
            help=help,
            hidden=hidden,
            show_choices=show_choices,
            show_envvar=show_envvar,
            **attrs,
        )

    def process_value(self, ctx: Context, value: Any) -> Optional[Path]:
        """Process the value of the option."""
        value = super().process_value(ctx, value)
        return resolve_conf_location(value) if value else None


def config_option(*param_decls: str, cls: Optional[type[ConfigOption]] = None, **attrs: Any) -> Callable[[FC], FC]:
    """
    Attaches a ConfigOption to the command.

    All positional arguments are passed as parameter declarations to `ConfigOption`.

    All keyword arguments are forwarded unchanged (except ``cls``). This is equivalent to creating a
    `ConfigOption` instance manually and attaching it to the `Command.params` list.

    For the default option class, refer to `ConfigOption` and `Parameter` for descriptions of parameters.

    Args:
        *param_decls: Passed as positional arguments to the constructor of `cls`.
        cls: the option class to instantiate.  This defaults to `ConfigOption`.
        **attrs: Passed as keyword arguments to the constructor of `cls`.

    Returns:
        A decorated function.
    """
    if cls is None:  # pragma: no-coverage
        cls = ConfigOption

    def decorator(f: FC) -> FC:
        _param_memo(f, cls(param_decls, **attrs))
        return f

    return decorator


def resolve_conf_location(url_or_path: str) -> Path:
    """Resolve a URL or path.

    The path is considered a URL if it is parseable as such and starts with ``http://`` or ``https://``.

    Args:
        url_or_path: The URL or path to resolve.

    Raises:
        BumpVersionError: if the file does not exist.

    Returns:
        The contents of the location.
    """
    parsed_url = urlparse(url_or_path)

    if parsed_url.scheme in ("http", "https"):
        return download_url(url_or_path)

    path = Path(url_or_path)
    if not path.exists():
        raise BumpVersionError(f"'{path}' does not exist.")
    return path


def download_url(url: str) -> Path:
    """
    Download the contents of a URL.

    Args:
        url: The URL to download

    Returns:
        The Path to the downloaded file.

    Raises:
        BadInputError: if there is a problem downloading the URL
    """
    logger.debug(f"Downloading configuration from URL: {url}")
    filename = get_file_name_from_url(url)
    suffix = Path(filename).suffix

    try:
        resp = httpx.get(url, follow_redirects=True, timeout=1)
        resp.raise_for_status()
        with NamedTemporaryFile(mode="w", delete=False, encoding="utf-8", suffix=suffix) as tmp:
            tmp.write(resp.text)
        return Path(tmp.name)
    except httpx.RequestError as e:
        raise BadInputError(f"Unable to download configuration from URL: {url}") from e
    except httpx.HTTPStatusError as e:
        msg = f"Error response {e.response.status_code} while requesting {url}."
        raise BadInputError(msg) from e


def get_file_name_from_url(url: str) -> str:
    """
    Extracts the file name from a URL.

    Args:
        url: The URL to extract the file name from.

    Returns:
        The file name from the URL, or an empty string if there is no file name.
    """
    parsed_url = urlparse(url)

    return parsed_url.path.split("/")[-1]
