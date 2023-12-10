import pytest

from bumpversion.indented_logger import IndentedLoggerAdapter
import logging


class TestIndentedLogger:
    def test_does_not_indent_without_intent(self, caplog: pytest.LogCaptureFixture):
        caplog.set_level(logging.DEBUG)
        logger = IndentedLoggerAdapter(logging.getLogger(), reset=True)
        logger.debug("test debug")
        logger.info("test info")
        logger.warning("test warning")
        logger.error("test error")
        logger.critical("test critical")

        assert caplog.record_tuples == [
            ("root", 10, "test debug"),
            ("root", 20, "test info"),
            ("root", 30, "test warning"),
            ("root", 40, "test error"),
            ("root", 50, "test critical"),
        ]

    def test_indents(self, caplog: pytest.LogCaptureFixture):
        caplog.set_level(logging.DEBUG)
        logger = IndentedLoggerAdapter(logging.getLogger(), reset=True)
        logger.info("test 1")
        logger.indent(2)
        logger.error("test %d", 2)
        logger.indent()
        logger.debug("test 3")
        logger.warning("test 4")
        logger.indent()
        logger.critical("test 5")
        logger.critical("test 6")

        assert caplog.record_tuples == [
            ("root", 20, "test 1"),
            ("root", 40, "    test 2"),
            ("root", 10, "      test 3"),
            ("root", 30, "      test 4"),
            ("root", 50, "        test 5"),
            ("root", 50, "        test 6"),
        ]

    def test_dedents(self, caplog: pytest.LogCaptureFixture):
        caplog.set_level(logging.DEBUG)
        logger = IndentedLoggerAdapter(logging.getLogger(), reset=True)
        logger.indent(3)
        logger.info("test 1")
        logger.dedent(2)
        logger.error("test %d", 2)
        logger.dedent()
        logger.debug("test 3")
        logger.warning("test 4")

        assert caplog.record_tuples == [
            ("root", 20, "      test 1"),
            ("root", 40, "  test 2"),
            ("root", 10, "test 3"),
            ("root", 30, "test 4"),
        ]

    def test_cant_dedent_below_zero(self, caplog: pytest.LogCaptureFixture):
        caplog.set_level(logging.DEBUG)
        logger = IndentedLoggerAdapter(logging.getLogger())
        logger.dedent(4)
        logger.info("test 1")

        assert caplog.record_tuples == [("root", 20, "test 1")]
