import pytest
from unittest.mock import patch, MagicMock, AsyncMock

import main


class TestMcpServer:
    """Test class for the MCP server functionality."""

    def test_check_driver_function(self):
        """Test the check_driver function when no driver is initialized."""
        # Save the original driver value
        original_driver = main.driver
        
        try:
            # Set driver to None
            main.driver = None
            
            # Test that check_driver raises an exception
            with pytest.raises(Exception) as excinfo:
                main.check_driver()
            
            assert "Appium driver not initialized" in str(excinfo.value)
        finally:
            # Restore the original driver value
            main.driver = original_driver

    def test_check_driver_function_with_driver(self):
        """Test the check_driver function when a driver is initialized."""
        # Save the original driver value
        original_driver = main.driver
        
        try:
            # Set driver to a mock
            main.driver = MagicMock()
            
            # This should not raise an exception
            main.check_driver()
        finally:
            # Restore the original driver value
            main.driver = original_driver
