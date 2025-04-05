import pytest
from unittest.mock import patch, MagicMock, AsyncMock

import main


# Mark all tests in this module as asyncio tests
pytestmark = pytest.mark.asyncio


class TestGestureTools:
    """Test class for the gesture tools in the main module."""

    async def test_swipe(self):
        """Test the swipe function."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver:
            # Call the function
            result = await main.swipe(100, 200, 300, 400, 500)
            
            # Check the result
            assert result["success"] is True
            assert "Swiped from (100, 200) to (300, 400)" in result["message"]
            
            # Check that the driver's swipe method was called with the correct arguments
            mock_driver.swipe.assert_called_once_with(100, 200, 300, 400, 500)
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()

    async def test_swipe_exception(self):
        """Test the swipe function when an exception occurs."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver:
            # Setup the mock to raise an exception
            mock_driver.swipe.side_effect = Exception("Test error")
            
            # Call the function
            result = await main.swipe(100, 200, 300, 400, 500)
            
            # Check the result
            assert "error" in result
            assert "Test error" in result["error"]
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()

    async def test_scroll_to_element(self):
        """Test the scroll_to_element function."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.AppiumBy') as mock_appium_by:
            # Setup the mocks
            mock_appium_by.ID = "id"
            mock_element = MagicMock()
            mock_driver.find_element.return_value = mock_element
            mock_driver.get_window_size.return_value = {"width": 400, "height": 800}
            
            # Call the function
            result = await main.scroll_to_element("id", "test-id", "down", 3)
            
            # Check the result
            assert result["success"] is True
            assert "Found element after 0 swipes" in result["message"]
            assert "element" in result
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's find_element method was called with the correct arguments
            mock_driver.find_element.assert_called_once_with("id", "test-id")
            
            # Check that the driver's get_window_size method was called
            mock_driver.get_window_size.assert_called_once()
            
            # Check that the driver's swipe method was not called (element found on first try)
            mock_driver.swipe.assert_not_called()

    async def test_scroll_to_element_with_swipes(self):
        """Test the scroll_to_element function with multiple swipes."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.AppiumBy') as mock_appium_by:
            # Setup the mocks
            mock_appium_by.ID = "id"
            mock_element = MagicMock()
            
            # Make find_element raise an exception twice, then return an element
            mock_driver.find_element.side_effect = [
                Exception("Element not found"),
                Exception("Element not found"),
                mock_element
            ]
            
            mock_driver.get_window_size.return_value = {"width": 400, "height": 800}
            
            # Call the function
            result = await main.scroll_to_element("id", "test-id", "down", 3)
            
            # Check the result
            assert result["success"] is True
            assert "Found element after 2 swipes" in result["message"]
            assert "element" in result
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's find_element method was called 3 times
            assert mock_driver.find_element.call_count == 3
            
            # Check that the driver's get_window_size method was called
            mock_driver.get_window_size.assert_called_once()
            
            # Check that the driver's swipe method was called twice
            assert mock_driver.swipe.call_count == 2

    async def test_scroll_to_element_not_found(self):
        """Test the scroll_to_element function when the element is not found."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.AppiumBy') as mock_appium_by:
            # Setup the mocks
            mock_appium_by.ID = "id"
            
            # Make find_element always raise an exception
            mock_driver.find_element.side_effect = Exception("Element not found")
            
            mock_driver.get_window_size.return_value = {"width": 400, "height": 800}
            
            # Call the function
            result = await main.scroll_to_element("id", "test-id", "down", 3)
            
            # Check the result
            assert result["success"] is False
            assert "Element not found after 3 swipes" in result["message"]
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's find_element method was called 3 times
            assert mock_driver.find_element.call_count == 3
            
            # Check that the driver's get_window_size method was called
            mock_driver.get_window_size.assert_called_once()
            
            # Check that the driver's swipe method was called 3 times
            assert mock_driver.swipe.call_count == 3

    async def test_pinch(self):
        """Test the pinch function."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.ActionChains') as mock_action_chains, \
             patch('main.ActionBuilder') as mock_action_builder, \
             patch('main.PointerInput') as mock_pointer_input, \
             patch('main.interaction') as mock_interaction:
            # Setup the mocks
            mock_interaction.POINTER_TOUCH = "touch"
            mock_actions = MagicMock()
            mock_action_chains.return_value = mock_actions
            mock_driver.get_window_size.return_value = {"width": 400, "height": 800}
            
            # Call the function
            result = await main.pinch()
            
            # Check the result
            assert result["success"] is True
            assert "Pinched screen by" in result["message"]
            assert "50" in result["message"]
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's get_window_size method was called
            mock_driver.get_window_size.assert_called_once()
            
            # Check that the actions were performed
            mock_actions.perform.assert_called_once()

    async def test_pinch_with_element(self):
        """Test the pinch function with an element."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.ActionChains') as mock_action_chains, \
             patch('main.ActionBuilder') as mock_action_builder, \
             patch('main.PointerInput') as mock_pointer_input, \
             patch('main.interaction') as mock_interaction, \
             patch('main.AppiumBy') as mock_appium_by:
            # Setup the mocks
            mock_interaction.POINTER_TOUCH = "touch"
            mock_appium_by.ID = "id"
            mock_element = MagicMock()
            mock_element.rect = {"x": 50, "y": 100, "width": 200, "height": 100}
            mock_driver.find_element.return_value = mock_element
            mock_actions = MagicMock()
            mock_action_chains.return_value = mock_actions
            
            # Call the function
            result = await main.pinch("id", "test-id", 75, 5)
            
            # Check the result
            assert result["success"] is True
            assert "Pinched element test-id by 75%" in result["message"]
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's find_element method was called
            mock_driver.find_element.assert_called_once_with("id", "test-id")
            
            # Check that the actions were performed
            mock_actions.perform.assert_called_once()

    async def test_zoom(self):
        """Test the zoom function."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.ActionChains') as mock_action_chains, \
             patch('main.ActionBuilder') as mock_action_builder, \
             patch('main.PointerInput') as mock_pointer_input, \
             patch('main.interaction') as mock_interaction:
            # Setup the mocks
            mock_interaction.POINTER_TOUCH = "touch"
            mock_actions = MagicMock()
            mock_action_chains.return_value = mock_actions
            mock_driver.get_window_size.return_value = {"width": 400, "height": 800}
            
            # Call the function
            result = await main.zoom()
            
            # Check the result
            assert result["success"] is True
            assert "Zoomed screen by" in result["message"]
            assert "200" in result["message"]
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's get_window_size method was called
            mock_driver.get_window_size.assert_called_once()
            
            # Check that the actions were performed
            mock_actions.perform.assert_called_once()

    async def test_zoom_with_element(self):
        """Test the zoom function with an element."""
        with patch('main.driver') as mock_driver, \
             patch('main.check_driver') as mock_check_driver, \
             patch('main.ActionChains') as mock_action_chains, \
             patch('main.ActionBuilder') as mock_action_builder, \
             patch('main.PointerInput') as mock_pointer_input, \
             patch('main.interaction') as mock_interaction, \
             patch('main.AppiumBy') as mock_appium_by:
            # Setup the mocks
            mock_interaction.POINTER_TOUCH = "touch"
            mock_appium_by.ID = "id"
            mock_element = MagicMock()
            mock_element.rect = {"x": 50, "y": 100, "width": 200, "height": 100}
            mock_driver.find_element.return_value = mock_element
            mock_actions = MagicMock()
            mock_action_chains.return_value = mock_actions
            
            # Call the function
            result = await main.zoom("id", "test-id", 150, 8)
            
            # Check the result
            assert result["success"] is True
            assert "Zoomed element test-id by 150%" in result["message"]
            
            # Check that check_driver was called
            mock_check_driver.assert_called_once()
            
            # Check that the driver's find_element method was called
            mock_driver.find_element.assert_called_once_with("id", "test-id")
            
            # Check that the actions were performed
            mock_actions.perform.assert_called_once()
