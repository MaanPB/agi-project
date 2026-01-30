"""
Unit tests for logging functionality
"""

import pytest
import json
import logging
from pathlib import Path
import tempfile

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agi_core.logger import (
    get_logger,
    JSONFormatter,
    ContextLogger,
    get_context_logger,
    setup_logging
)


class TestGetLogger:
    """Tests for get_logger function"""
    
    def test_get_logger_basic(self):
        """Test basic logger creation"""
        logger = get_logger("test_logger")
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
    
    def test_get_logger_custom_level(self):
        """Test logger with custom level"""
        logger = get_logger("test_debug", level="DEBUG")
        assert logger.level == logging.DEBUG
        
        logger = get_logger("test_error", level="ERROR")
        assert logger.level == logging.ERROR
    
    def test_get_logger_with_file(self, tmp_path):
        """Test logger with file output"""
        log_file = tmp_path / "test.log"
        logger = get_logger("test_file_logger", log_file=str(log_file))
        
        logger.info("Test message")
        
        assert log_file.exists()
    
    def test_logger_json_format(self, capsys):
        """Test that logger outputs valid JSON"""
        logger = get_logger("test_json", format_type="json")
        logger.info("Test message")
        
        captured = capsys.readouterr()
        
        # Should be valid JSON
        try:
            log_data = json.loads(captured.out.strip())
            assert log_data["message"] == "Test message"
            assert log_data["level"] == "INFO"
            assert "timestamp" in log_data
        except json.JSONDecodeError:
            pytest.fail("Logger output is not valid JSON")


class TestJSONFormatter:
    """Tests for JSONFormatter"""
    
    def test_json_formatter_basic(self):
        """Test basic JSON formatting"""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        output = formatter.format(record)
        log_data = json.loads(output)
        
        assert log_data["message"] == "Test message"
        assert log_data["level"] == "INFO"
        assert log_data["name"] == "test"
        assert "timestamp" in log_data
    
    def test_json_formatter_with_correlation_id(self):
        """Test JSON formatter with correlation ID"""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        record.correlation_id = "test-correlation-id-123"
        
        output = formatter.format(record)
        log_data = json.loads(output)
        
        assert log_data["correlation_id"] == "test-correlation-id-123"
    
    def test_json_formatter_with_extra_fields(self):
        """Test JSON formatter with extra fields"""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        record.extra_fields = {"user_id": 123, "session": "abc"}
        
        output = formatter.format(record)
        log_data = json.loads(output)
        
        assert log_data["user_id"] == 123
        assert log_data["session"] == "abc"


class TestContextLogger:
    """Tests for ContextLogger"""
    
    def test_context_logger_basic(self):
        """Test basic context logger functionality"""
        base_logger = get_logger("test_context")
        context_logger = ContextLogger(base_logger, correlation_id="test-123")
        
        assert context_logger.correlation_id == "test-123"
    
    def test_context_logger_auto_correlation_id(self):
        """Test that context logger generates correlation ID if not provided"""
        base_logger = get_logger("test_auto_id")
        context_logger = ContextLogger(base_logger)
        
        assert context_logger.correlation_id is not None
        assert len(context_logger.correlation_id) > 0
    
    def test_context_logger_extra_fields(self):
        """Test context logger with extra fields"""
        base_logger = get_logger("test_extra")
        context_logger = ContextLogger(
            base_logger,
            correlation_id="test-456",
            user_id=789,
            session="xyz"
        )
        
        assert context_logger.extra_fields["user_id"] == 789
        assert context_logger.extra_fields["session"] == "xyz"


class TestGetContextLogger:
    """Tests for get_context_logger function"""
    
    def test_get_context_logger(self):
        """Test creating context logger"""
        logger = get_context_logger("test_get_context", user_id=123)
        
        assert isinstance(logger, ContextLogger)
        assert logger.extra_fields["user_id"] == 123


class TestSetupLogging:
    """Tests for setup_logging function"""
    
    def test_setup_logging_basic(self):
        """Test basic logging setup"""
        config = {
            "logging": {
                "level": "DEBUG",
                "format": "json"
            }
        }
        
        # Should not raise any exceptions
        setup_logging(config)
    
    def test_setup_logging_with_file(self, tmp_path):
        """Test logging setup with file"""
        log_file = tmp_path / "setup_test.log"
        config = {
            "logging": {
                "level": "INFO",
                "file": str(log_file)
            }
        }
        
        setup_logging(config)
        
        # Get the logger and log something
        logger = get_logger("agi_core")
        logger.info("Test after setup")
        
        # File should be created (though we can't easily verify content in this test)
        assert log_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
