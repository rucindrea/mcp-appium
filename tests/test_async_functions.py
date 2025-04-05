import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

import main


# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio


class TestAsyncFunctions:
    """Test class for the async functions in the main module."""

    async def test_start_appium_server(self):
        """Test the start_appium_server async function."""
        # Import subprocess directly in the test
        import subprocess
        
        # Save the original Popen
        original_popen = subprocess.Popen
        
        try:
            # Create a mock Popen
            mock_popen = MagicMock()
            process_mock = MagicMock()
            process_mock.poll.return_value = None  # Process is running
            mock_popen.return_value = process_mock
            
            # Replace the original Popen with our mock
            subprocess.Popen = mock_popen
            
            # Call the async function
            result = await main.start_appium_server()
            
            # Check the result
            assert "Appium server started successfully" in result
        finally:
            # Restore the original Popen
            subprocess.Popen = original_popen

    async def test_create_android_driver(self):
        """Test the create_android_driver async function."""
        with patch('main.webdriver.Remote') as mock_remote:
            # Setup the mock
            mock_remote.return_value = MagicMock()

            # Call the async function
            result = await main.create_android_driver(
                app_path="test_app.apk",
                device_name="Test Device",
                platform_version="10.0"
            )

            # Check the result
            assert "Appium driver created successfully" in result

    async def test_find_element(self):
        """Test the find_element async function."""
        with patch('main.driver') as mock_driver, \
             patch('main.WebDriverWait') as mock_wait:
            # Setup the mocks
            mock_element = MagicMock()
            mock_element.id = "element-id"
            mock_element.location = {"x": 10, "y": 20}
            mock_element.size = {"width": 100, "height": 50}
            mock_element.text = "Test Element"
            mock_element.tag_name = "button"
            mock_element.is_displayed.return_value = True
            mock_element.is_enabled.return_value = True
            mock_element.get_attribute.side_effect = lambda attr: {
                "resource-id": "test-id",
                "content-desc": "test-desc",
                "text": "Test Element",
                "class": "android.widget.Button",
                "enabled": "true",
                "displayed": "true"
            }.get(attr, None)

            mock_wait_instance = MagicMock()
            mock_wait_instance.until.return_value = mock_element
            mock_wait.return_value = mock_wait_instance

            # Call the async function
            result = await main.find_element("id", "test-id")

            # Check the result
            assert result["id"] == "element-id"
            assert result["text"] == "Test Element"
            assert result["tag_name"] == "button"
            assert result["is_displayed"] is True
            assert result["is_enabled"] is True

    async def test_tap_element(self):
        """Test the tap_element async function."""
        with patch('main.driver') as mock_driver, \
             patch('main.WebDriverWait') as mock_wait:
            # Setup the mocks
            mock_element = MagicMock()
            mock_wait_instance = MagicMock()
            mock_wait_instance.until.return_value = mock_element
            mock_wait.return_value = mock_wait_instance

            # Call the async function
            result = await main.tap_element("id", "test-id")

            # Check the result
            assert result["success"] is True
            assert "Tapped element test-id" in result["message"]
            mock_element.click.assert_called_once()

    async def test_set_text(self):
        """Test the set_text async function."""
        with patch('main.driver') as mock_driver, \
             patch('main.WebDriverWait') as mock_wait:
            # Setup the mocks
            mock_element = MagicMock()
            mock_wait_instance = MagicMock()
            mock_wait_instance.until.return_value = mock_element
            mock_wait.return_value = mock_wait_instance

            # Call the async function
            result = await main.set_text("id", "test-id", "Test Text", True)

            # Check the result
            assert result["success"] is True
            assert "Set text 'Test Text' on element test-id" in result["message"]
            mock_element.clear.assert_called_once()
            mock_element.send_keys.assert_called_once_with("Test Text")

    async def test_take_screenshot(self):
        """Test the take_screenshot async function."""
        with patch('main.driver') as mock_driver:
            # Setup the mock
            mock_driver.get_screenshot_as_base64.return_value = "base64-screenshot-data"

            # Call the async function
            result = await main.take_screenshot()

            # Check the result
            assert result["success"] is True
            assert result["screenshot"] == "base64-screenshot-data"

    async def test_stop_appium_driver(self):
        """Test the stop_appium_driver async function."""
        # Test with driver initialized
        with patch('main.driver') as mock_driver:
            # Call the async function
            result = await main.stop_appium_driver()

            # Check the result
            assert result["success"] is True
            assert "Appium driver stopped successfully" in result["message"]
            mock_driver.quit.assert_called_once()

        # Test with no driver initialized
        main.driver = None
        result = await main.stop_appium_driver()
        assert result["success"] is False
        assert "Appium driver is not running" in result["message"]

    async def test_set_test_name(self):
        """Test the set_test_name async function."""
        with patch('main.test_info') as mock_test_info:
            # Call the async function
            result = await main.set_test_name("Test Name")

            # Check the result
            assert result["success"] is True
            assert "Test name set to: Test Name" in result["message"]
            mock_test_info.__setitem__.assert_called_once_with("name", "Test Name")
