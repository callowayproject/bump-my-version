"""Tests for the yaml serialization module."""

from pathlib import Path

from bumpversion import yaml_dump
from datetime import datetime, date


def test_dump_unknown():
    assert yaml_dump.dump({1, 2}) == '"{1, 2}"'


def test_format_str():
    assert yaml_dump.format_str("value") == '"value"'


def test_format_int():
    assert yaml_dump.format_int(10) == "10"


def test_format_float():
    assert yaml_dump.format_float(1.0) == "1.0"
    assert yaml_dump.format_float(1e300) == ".inf"
    assert yaml_dump.format_float(-1e300) == "-.inf"
    assert yaml_dump.format_float(1e17) == "1.0e+17"
    assert yaml_dump.format_float(float("nan")) == ".nan"


def test_format_bool():
    assert yaml_dump.format_bool(True) == "true"
    assert yaml_dump.format_bool(False) == "false"


def test_format_dict():
    test_dict = {
        "key": "strval",
        "key2": 30,
        "key3": datetime(2023, 6, 19, 13, 45, 30),
        "key4": date(2023, 6, 19),
        "key5": {"subkey": "subval"},
        "key6": [1, 2, 3],
        "key7": None,
        "key8": True,
        "key9": False,
        "key10": 1.43,
        "key11": (1, 2, 3),
    }
    expected = (
        'key: "strval"\n'
        "key10: 1.43\n"
        "key11:\n"
        "  - 1\n"
        "  - 2\n"
        "  - 3\n"
        "key2: 30\n"
        "key3: 2023-06-19 13:45:30\n"
        "key4: 2023-06-19\n"
        "key5:\n"
        '  subkey: "subval"\n'
        "key6:\n"
        "  - 1\n"
        "  - 2\n"
        "  - 3\n"
        "key7: null\n"
        "key8: true\n"
        "key9: false\n"
    )
    assert yaml_dump.format_dict(test_dict) == expected


def test_format_list():
    assert yaml_dump.format_sequence(["item"]) == '- "item"\n'
    assert yaml_dump.format_sequence(["item", ["item2"]]) == '- "item"\n-\n  - "item2"\n'
    assert yaml_dump.format_sequence(("item",)) == '- "item"\n'
    assert yaml_dump.format_sequence(("item", ("item2",))) == '- "item"\n-\n  - "item2"\n'


def test_dump_none_val():
    assert yaml_dump.format_none(None) == "null"


def test_dump_date_val():
    test_date = date(2023, 6, 19)
    assert yaml_dump.format_date(test_date) == "2023-06-19"


def test_dump_datetime_val():
    test_datetime = datetime(2023, 6, 19, 13, 45, 30)
    assert yaml_dump.format_datetime(test_datetime) == "2023-06-19 13:45:30"
