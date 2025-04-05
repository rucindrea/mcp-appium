import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import traceback

import main


class TestErrorHandling:
    """Test class for error handling in the main module."""

    def test_on_error_handler(self):
        """Test the custom error handler for the MCP server."""
        with patch('main.logger') as mock_logger:
            # Create a test error
            test_error = Exception("Test error")
            
            # Call the error handler
            main.on_error(test_error)
            
            # Check that the error was logged
            mock_logger.error.assert_any_call(f"MCP server error: {test_error}")
            mock_logger.error.assert_any_call(traceback.format_exc())

    @patch('main.driver', None)
    def test_check_driver_no_driver(self):
        """Test the check_driver function when no driver is initialized."""
        with pytest.raises(Exception) as excinfo:
            main.check_driver()
        
        assert "Appium driver not initialized" in str(excinfo.value)

    @patch('main.driver', MagicMock())
    def test_check_driver_with_driver(self):
        """Test the check_driver function when a driver is initialized."""
        # This should not raise an exception
        main.check_driver()

    @pytest.mark.asyncio
    async def test_start_appium_server_exception(self):
        """Test the start_appium_server function when an exception occurs."""
        with patch('subprocess.Popen', side_effect=Exception("Test error")), \
             patch('main.logger') as mock_logger:
            
            # Call the function
            result = await main.start_appium_server()
            
            # Check the result
            assert "Failed to start Appium server" in result
            assert "Test error" in result
            
            # Check that the error was logged
            mock_logger.error.assert_any_call("Failed to start Appium server: Test error")

    @pytest.mark.asyncio
    async def test_create_android_driver_exception(self):
        """Test the create_android_driver function when an exception occurs."""
        with patch('main.webdriver.Remote', side_effect=Exception("Test error")), \
             patch('main.logger') as mock_logger:
            
            # Call the function
            result = await main.create_android_driver(app_path="test_app.apk")
            
            # Check the result
            assert "Failed to create Appium driver" in result
            assert "Test error" in result
            
            # Check that the error was logged
            mock_logger.error.assert_any_call("Failed to create Appium driver: Test error")

    @pytest.mark.asyncio
    async def test_find_element_exception(self):
        """Test the find_element function when an exception occurs."""
        with patch('main.driver', MagicMock()), \
             patch('main.WebDriverWait', side_effect=Exception("Test error")):
            
            # Call the function
            result = await main.find_element("id", "test-id")
            
            # Check the result
            assert "error" in result
            assert "Test error" in result["error"]

    @pytest.mark.asyncio
    async def test_tap_element_exception(self):
        """Test the tap_element function when an exception occurs."""
        with patch('main.driver', MagicMock()), \
             patch('main.WebDriverWait', side_effect=Exception("Test error")):
            
            # Call the function
            result = await main.tap_element("id", "test-id")
            
            # Check the result
            assert "error" in result
            assert "Test error" in result["error"]

    @pytest.mark.asyncio
    async def test_stop_appium_driver_exception(self):
        """Test the stop_appium_driver function when an exception occurs."""
        mock_driver = MagicMock()
        mock_driver.quit.side_effect = Exception("Test error")
        
        with patch('main.driver', mock_driver), \
             patch('main.logger') as mock_logger:
            
            # Call the function
            result = await main.stop_appium_driver()
            
            # Check the result
            assert "error" in result
            assert "Test error" in result["error"]
            
            # Check that the error was logged
            mock_logger.error.assert_any_call("Error stopping Appium driver: Test error")

    def test_element_to_dict_exception(self):
        """Test the element_to_dict function when an exception occurs."""
        # Create a mock element that raises an exception
        mock_element = MagicMock()
        mock_element.id = "element-id"
        mock_element.location = MagicMock(side_effect=Exception("Test error"))
        mock_element.get_attribute.side_effect = Exception("Test error")
        mock_element.is_displayed.side_effect = Exception("Test error")
        mock_element.is_enabled.side_effect = Exception("Test error")
        
        # Mock the logger to prevent actual logging
        with patch('main.logger') as mock_logger:
            # Call the function
            result = main.element_to_dict(mock_element)
            
            # Check the result
            assert result["id"] == "element-id"
            assert "error" in result
            assert "Test error" in result["error"]
