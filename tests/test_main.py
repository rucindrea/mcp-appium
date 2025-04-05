import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock

# Import the module to test
import main


class TestAppiumMCP:
    """Test class for the Appium MCP server."""

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_start_appium_server_success(self, mock_popen):
        """Test starting the Appium server successfully."""
        # Setup the mock
        process_mock = MagicMock()
        process_mock.poll.return_value = None  # Process is running
        mock_popen.return_value = process_mock

        # Call the function
        result = await main.start_appium_server()

        # Check the result
        assert "Appium server started successfully" in result

    @pytest.mark.asyncio
    @patch('subprocess.Popen')
    async def test_start_appium_server_failure(self, mock_popen):
        """Test starting the Appium server with a failure."""
        # Setup the mock
        process_mock = MagicMock()
        process_mock.poll.return_value = 1  # Process exited with error
        process_mock.communicate.return_value = ("", "Failed to start")
        mock_popen.return_value = process_mock

        # Call the function
        result = await main.start_appium_server()

        # Check the result
        assert "Failed to start Appium server" in result

    @pytest.mark.asyncio
    @patch('main.webdriver.Remote')
    async def test_create_android_driver_success(self, mock_remote):
        """Test creating an Android driver successfully."""
        # Setup the mock
        mock_remote.return_value = MagicMock()

        # Call the function
        result = await main.create_android_driver(
            app_path="test_app.apk",
            device_name="Test Device",
            platform_version="10.0"
        )

        # Check the result
        assert "Appium driver created successfully" in result
        assert main.driver is not None

    @pytest.mark.asyncio
    @patch('main.webdriver.Remote')
    async def test_create_android_driver_missing_params(self, mock_remote):
        """Test creating an Android driver with missing parameters."""
        # Call the function without required parameters
        result = await main.create_android_driver()

        # Check the result
        assert "Either app_path or both app_package and app_activity must be provided" in result

    @pytest.mark.asyncio
    @patch('main.webdriver.Remote', side_effect=Exception("Connection error"))
    async def test_create_android_driver_exception(self, mock_remote):
        """Test creating an Android driver with an exception."""
        # Call the function
        result = await main.create_android_driver(app_path="test_app.apk")

        # Check the result
        assert "Failed to create Appium driver" in result
        assert "Connection error" in result

    # Similar tests for iOS and Mac drivers can be added here

    @pytest.mark.asyncio
    @patch('main.driver')
    async def test_find_element_success(self, mock_driver):
        """Test finding an element successfully."""
        # Setup the mock
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

        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_element
        main.WebDriverWait = MagicMock(return_value=mock_wait)
        main.driver = mock_driver

        # Call the function
        result = await main.find_element("id", "test-id")

        # Check the result
        assert result["id"] == "element-id"
        assert result["text"] == "Test Element"
        assert result["tag_name"] == "button"
        assert result["is_displayed"] is True
        assert result["is_enabled"] is True

    @pytest.mark.asyncio
    @patch('main.driver', None)
    @patch('main.check_driver', side_effect=Exception("Appium driver not initialized"))
    async def test_find_element_no_driver(self, mock_check_driver):
        """Test finding an element with no driver initialized."""
        # Call the function
        with pytest.raises(Exception) as excinfo:
            await main.find_element("id", "test-id")

        # Check the exception
        assert "Appium driver not initialized" in str(excinfo.value)

    # Add more tests for other functions here

    def test_element_to_dict(self):
        """Test converting a WebElement to a dictionary."""
        # Create a mock element
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

        # Call the function
        result = main.element_to_dict(mock_element)

        # Check the result
        assert result["id"] == "element-id"
        assert result["location"] == {"x": 10, "y": 20}
        assert result["size"] == {"width": 100, "height": 50}
        assert result["text"] == "Test Element"
        assert result["tag_name"] == "button"
        assert result["is_displayed"] is True
        assert result["is_enabled"] is True
        assert result["attributes"]["resource-id"] == "test-id"
        assert result["attributes"]["content-desc"] == "test-desc"

    def test_element_to_dict_none(self):
        """Test converting None to a dictionary."""
        # Call the function with None
        result = main.element_to_dict(None)

        # Check the result
        assert result is None

    def test_element_to_dict_exception(self):
        """Test converting an element that raises an exception."""
        # Create a mock element that raises an exception
        mock_element = MagicMock()
        mock_element.id = "element-id"
        mock_element.location = MagicMock(side_effect=Exception("Test error"))
        mock_element.get_attribute.side_effect = Exception("Test error")
        mock_element.is_displayed.side_effect = Exception("Test error")
        mock_element.is_enabled.side_effect = Exception("Test error")
        
        # Mock the logger to prevent actual logging
        with patch('main.logger'):
            # Call the function
            result = main.element_to_dict(mock_element)
            
            # Check the result
            assert result["id"] == "element-id"
            assert "error" in result
            assert "Test error" in result["error"]

    # Add more tests for utility functions
