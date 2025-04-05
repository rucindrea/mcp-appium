import pytest
from unittest.mock import patch, MagicMock
import datetime

import main


class TestActionLogging:
    """Test class for the action logging functionality."""

    def setup_method(self):
        """Reset the action log and test info before each test."""
        main.action_log = []
        main.test_info = {
            "name": "Unnamed Test",
            "started_at": None,
            "finished_at": None,
            "status": "Not Started",
            "success_count": 0,
            "error_count": 0,
        }

    def test_log_action_first_action(self):
        """Test logging the first action."""
        # Log the first action
        main.log_action("test_action", {"test": "data"}, True)

        # Check that the test start time was set
        assert main.test_info["started_at"] is not None
        assert main.test_info["status"] == "Running"
        assert main.test_info["success_count"] == 1
        assert main.test_info["error_count"] == 0

        # Check that the action was added to the log
        assert len(main.action_log) == 1
        assert main.action_log[0]["type"] == "test_action"
        assert main.action_log[0]["details"] == {"test": "data"}
        assert main.action_log[0]["success"] is True
        assert "timestamp" in main.action_log[0]

    def test_log_action_success(self):
        """Test logging a successful action."""
        # Set the test as already started
        main.test_info["started_at"] = datetime.datetime.now()
        main.test_info["status"] = "Running"

        # Log a successful action
        main.log_action("test_action", {"test": "data"}, True)

        # Check that the success count was incremented
        assert main.test_info["success_count"] == 1
        assert main.test_info["error_count"] == 0

        # Check that the action was added to the log
        assert len(main.action_log) == 1
        assert main.action_log[0]["success"] is True

    def test_log_action_failure(self):
        """Test logging a failed action."""
        # Set the test as already started
        main.test_info["started_at"] = datetime.datetime.now()
        main.test_info["status"] = "Running"

        # Log a failed action
        main.log_action("test_action", {"test": "data"}, False)

        # Check that the error count was incremented
        assert main.test_info["success_count"] == 0
        assert main.test_info["error_count"] == 1

        # Check that the action was added to the log
        assert len(main.action_log) == 1
        assert main.action_log[0]["success"] is False

    def test_complete_test_success(self):
        """Test completing a test successfully."""
        # Set the test as already started
        main.test_info["started_at"] = datetime.datetime.now()
        main.test_info["status"] = "Running"

        # Complete the test successfully
        main.complete_test(True)

        # Check that the test was marked as completed
        assert main.test_info["finished_at"] is not None
        assert main.test_info["status"] == "Completed Successfully"

    def test_complete_test_failure(self):
        """Test completing a test with errors."""
        # Set the test as already started
        main.test_info["started_at"] = datetime.datetime.now()
        main.test_info["status"] = "Running"

        # Complete the test with errors
        main.complete_test(False)

        # Check that the test was marked as completed with errors
        assert main.test_info["finished_at"] is not None
        assert main.test_info["status"] == "Completed with Errors"

    @pytest.mark.asyncio
    @patch('main.test_info')
    async def test_set_test_name(self, mock_test_info):
        """Test setting the test name."""
        # Call the function
        result = await main.set_test_name("Test Name")

        # Check that the test name was set
        mock_test_info.__setitem__.assert_called_once_with("name", "Test Name")

        # Check the result
        assert result["success"] is True
        assert "Test name set to: Test Name" in result["message"]
