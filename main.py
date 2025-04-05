#!/usr/bin/env python
import os
import json
import datetime
import logging
import sys
import traceback
from typing import Any, Dict, List, Optional, Union
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            os.path.expanduser("~/Library/Logs/Claude/mcp-server-appium.log")
        ),
    ],
)
logger = logging.getLogger("appium-mcp")
logger.info("Starting Appium MCP server")

try:
    # Initialize FastMCP server
    logger.info("Initializing FastMCP server")
    mcp = FastMCP("Appium")
    logger.info("FastMCP server initialized successfully")

    # Add more detailed logging for the connection process
    logger.debug("About to connect to transport")

    # Override the onerror handler to log errors
    def on_error(error):
        logger.error(f"MCP server error: {error}")
        logger.error(traceback.format_exc())

    mcp.onerror = on_error
    logger.debug("Set custom error handler")

except Exception as e:
    logger.error(f"Failed to initialize FastMCP server: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)

# Global variable to store the Appium driver instance
driver = None


@mcp.tool()
async def start_appium_server() -> str:
    """Start the Appium server on the host machine."""
    logger.info("Attempting to start Appium server")

    # Start the Appium server using subprocess
    import subprocess
    import time

    try:
        logger.info("Launching Appium server")
        # Start Appium server in the background
        process = subprocess.Popen(
            ["appium"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        # Wait a bit for the server to start
        time.sleep(5)
        
        # Check if the process is running
        if process.poll() is None:
            logger.info("Appium server started successfully")
            return "Appium server started successfully."
        else:
            stdout, stderr = process.communicate()
            logger.error(f"Failed to start Appium server: {stderr}")
            return f"Failed to start Appium server: {stderr}"
    except Exception as e:
        logger.error(f"Failed to start Appium server: {e}")
        logger.error(traceback.format_exc())
        return f"Failed to start Appium server: {e}"


@mcp.tool()
async def create_android_driver(
    app_path: str = None,
    device_name: str = "Android Emulator",
    platform_version: str = "10.0",
    app_package: str = None,
    app_activity: str = None,
    automation_name: str = "UiAutomator2",
    appium_server_url: str = "http://localhost:4723/wd/hub",
    no_reset: bool = False,
    full_reset: bool = False,
    auto_grant_permissions: bool = True,
) -> str:
    """Create an Appium driver instance for Android."""
    global driver

    logger.info("Creating Android Appium driver with parameters:")
    logger.info(f"  App Path: {app_path}")
    logger.info(f"  Device Name: {device_name}")
    logger.info(f"  Platform Version: {platform_version}")
    logger.info(f"  App Package: {app_package}")
    logger.info(f"  App Activity: {app_activity}")
    logger.info(f"  Automation Name: {automation_name}")
    logger.info(f"  Appium Server URL: {appium_server_url}")

    try:
        logger.info("Initializing Appium driver connection...")
        
        # Create capabilities using AppiumOptions
        from appium.options.android import UiAutomator2Options
        
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = device_name
        options.platform_version = platform_version
        options.automation_name = automation_name
        options.no_reset = no_reset
        options.full_reset = full_reset
        options.auto_grant_permissions = auto_grant_permissions
        
        # Add app path or app package/activity if provided
        if app_path:
            options.app = app_path
        elif app_package and app_activity:
            options.app_package = app_package
            options.app_activity = app_activity
        else:
            return "Either app_path or both app_package and app_activity must be provided."
        
        logger.info(f"Using options: {options.capabilities}")
        
        # Create the driver with the options
        driver = webdriver.Remote(appium_server_url, options=options)
        logger.info("Appium driver connection established successfully")
    except Exception as e:
        error_msg = f"Failed to create Appium driver: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return error_msg

    # Return success message
    logger.info("Appium driver created successfully")
    return "Appium driver created successfully."


@mcp.tool()
async def create_ios_driver(
    app_path: str = None,
    device_name: str = "iPhone Simulator",
    platform_version: str = "15.0",
    bundle_id: str = None,
    automation_name: str = "XCUITest",
    appium_server_url: str = "http://localhost:4723/wd/hub",
    no_reset: bool = False,
    full_reset: bool = False,
    auto_accept_alerts: bool = True,
) -> str:
    """Create an Appium driver instance for iOS."""
    global driver

    logger.info("Creating iOS Appium driver with parameters:")
    logger.info(f"  App Path: {app_path}")
    logger.info(f"  Device Name: {device_name}")
    logger.info(f"  Platform Version: {platform_version}")
    logger.info(f"  Bundle ID: {bundle_id}")
    logger.info(f"  Automation Name: {automation_name}")
    logger.info(f"  Appium Server URL: {appium_server_url}")

    try:
        logger.info("Initializing Appium driver connection...")
        
        # Create capabilities using AppiumOptions
        from appium.options.ios import XCUITestOptions
        
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.device_name = device_name
        options.platform_version = platform_version
        options.automation_name = automation_name
        options.no_reset = no_reset
        options.full_reset = full_reset
        options.auto_accept_alerts = auto_accept_alerts
        
        # Add app path or bundle ID if provided
        if app_path:
            options.app = app_path
        elif bundle_id:
            options.bundle_id = bundle_id
        else:
            return "Either app_path or bundle_id must be provided."
        
        logger.info(f"Using options: {options.capabilities}")
        
        # Create the driver with the options
        driver = webdriver.Remote(appium_server_url, options=options)
        logger.info("Appium driver connection established successfully")
    except Exception as e:
        error_msg = f"Failed to create Appium driver: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return error_msg

    # Return success message
    logger.info("Appium driver created successfully")
    return "Appium driver created successfully."


@mcp.tool()
async def create_mac_driver(
    app_path: str = None,
    bundle_id: str = None,
    app_name: str = None,
    automation_name: str = "Mac2",
    appium_server_url: str = "http://localhost:4723/wd/hub",
) -> str:
    """Create an Appium driver instance for macOS desktop applications."""
    global driver

    logger.info("Creating macOS Appium driver with parameters:")
    logger.info(f"  App Path: {app_path}")
    logger.info(f"  Bundle ID: {bundle_id}")
    logger.info(f"  App Name: {app_name}")
    logger.info(f"  Automation Name: {automation_name}")
    logger.info(f"  Appium Server URL: {appium_server_url}")

    try:
        logger.info("Initializing Appium driver connection...")
        
        # Create capabilities using AppiumOptions
        from appium.options.mac import Mac2Options
        
        options = Mac2Options()
        options.platform_name = "Mac"
        options.automation_name = automation_name
        
        # Add app path, bundle ID, or app name if provided
        if app_path:
            options.app = app_path
        elif bundle_id:
            options.bundle_id = bundle_id
        elif app_name:
            # For system applications or already installed applications
            options.app_name = app_name
        else:
            return "Either app_path, bundle_id, or app_name must be provided."
        
        logger.info(f"Using options: {options.capabilities}")
        
        # Create the driver with the options
        driver = webdriver.Remote(appium_server_url, options=options)
        logger.info("Appium driver connection established successfully")
    except Exception as e:
        error_msg = f"Failed to create Appium driver: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return error_msg

    # Return success message
    logger.info("Appium driver created successfully")
    return "Appium driver created successfully."


# Helper function to convert WebElement to dictionary
def element_to_dict(element) -> Dict:
    """Convert a WebElement to a dictionary for JSON serialization."""
    if element is None:
        return None

    try:
        # Get basic element properties
        element_id = element.id
        location = element.location
        size = element.size
        text = element.text
        tag_name = element.tag_name
        
        # Get element attributes
        attributes = {}
        try:
            attributes["resource-id"] = element.get_attribute("resource-id")
        except Exception:
            pass
        
        try:
            attributes["content-desc"] = element.get_attribute("content-desc")
        except Exception:
            pass
        
        try:
            attributes["text"] = element.get_attribute("text")
        except Exception:
            pass
        
        try:
            attributes["class"] = element.get_attribute("class")
        except Exception:
            pass
        
        try:
            attributes["enabled"] = element.get_attribute("enabled")
        except Exception:
            pass
        
        try:
            attributes["displayed"] = element.get_attribute("displayed")
        except Exception:
            pass

        return {
            "id": element_id,
            "location": location,
            "size": size,
            "text": text,
            "tag_name": tag_name,
            "attributes": attributes,
            "is_displayed": element.is_displayed() if hasattr(element, "is_displayed") else None,
            "is_enabled": element.is_enabled() if hasattr(element, "is_enabled") else None,
        }
    except Exception as e:
        logger.error(f"Error converting element to dict: {e}")
        return {
            "id": element.id if hasattr(element, "id") else "unknown",
            "error": str(e)
        }


# Helper function to check if driver is initialized
def check_driver() -> None:
    """Check if the Appium driver is initialized."""
    if driver is None:
        logger.error("Appium driver not initialized. Call create_android_driver, create_ios_driver, or create_mac_driver first.")
        raise Exception(
            "Appium driver not initialized. Call create_android_driver, create_ios_driver, or create_mac_driver first."
        )


# Find Elements Tools
@mcp.tool()
async def find_element(
    by: str, value: str, timeout: float = 10.0
) -> Dict:
    """Find the first element that matches the given criteria."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Use WebDriverWait to wait for the element to be present
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        return element_to_dict(element)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def find_elements(
    by: str, value: str, timeout: float = 10.0
) -> List[Dict]:
    """Find all elements that match the given criteria."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Use WebDriverWait to wait for at least one element to be present
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        # Get all matching elements
        elements = driver.find_elements(by_enum, value)
        
        return [element_to_dict(element) for element in elements]
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def wait_for_element(
    by: str, value: str, timeout: float = 20.0
) -> Dict:
    """Wait for an element to be present."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        return element_to_dict(element)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def wait_for_element_to_be_clickable(
    by: str, value: str, timeout: float = 20.0
) -> Dict:
    """Wait for an element to be clickable."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by_enum, value))
        )
        
        return element_to_dict(element)
    except Exception as e:
        return {"error": str(e)}


# Element Interaction Tools
@mcp.tool()
async def tap_element(
    by: str, value: str, timeout: float = 10.0
) -> Dict:
    """Tap on an element."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Wait for the element to be clickable
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by_enum, value))
        )
        
        # Tap on the element
        element.click()
        
        return {"success": True, "message": f"Tapped element {value}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def long_press_element(
    by: str, value: str, duration_ms: int = 1000, timeout: float = 10.0
) -> Dict:
    """Long press on an element."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Wait for the element to be present
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        # Get element location
        rect = element.rect
        center_x = rect['x'] + rect['width'] // 2
        center_y = rect['y'] + rect['height'] // 2
        
        # Create a W3C Actions sequence for long press
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_ms / 1000)  # Convert ms to seconds
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        
        return {"success": True, "message": f"Long pressed element {value} for {duration_ms}ms"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_text(
    by: str, value: str, timeout: float = 10.0
) -> Dict:
    """Get text from an element."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Wait for the element to be present
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        # Get the text
        text = element.text
        
        return {"success": True, "text": text}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def set_text(
    by: str, value: str, text: str, clear_first: bool = True, timeout: float = 10.0
) -> Dict:
    """Set text on an element."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Wait for the element to be present
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        # Clear the field if requested
        if clear_first:
            element.clear()
        
        # Set the text
        element.send_keys(text)
        
        return {"success": True, "message": f"Set text '{text}' on element {value}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_attribute(
    by: str, value: str, attribute: str, timeout: float = 10.0
) -> Dict:
    """Get an attribute from an element."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Wait for the element to be present
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by_enum, value))
        )
        
        # Get the attribute
        attr_value = element.get_attribute(attribute)
        
        return {"success": True, "attribute": attribute, "value": attr_value}
    except Exception as e:
        return {"error": str(e)}


# Navigation and App Control Tools
@mcp.tool()
async def go_back() -> Dict:
    """Press the back button."""
    check_driver()

    try:
        driver.back()
        return {"success": True, "message": "Pressed back button"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def go_home() -> Dict:
    """Press the home button."""
    check_driver()

    try:
        driver.press_keycode(3)  # Android home button keycode
        return {"success": True, "message": "Pressed home button"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def launch_app() -> Dict:
    """Launch the app under test."""
    check_driver()

    try:
        driver.launch_app()
        return {"success": True, "message": "App launched"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def close_app() -> Dict:
    """Close the app under test."""
    check_driver()

    try:
        driver.close_app()
        return {"success": True, "message": "App closed"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def reset_app() -> Dict:
    """Reset the app under test."""
    check_driver()

    try:
        driver.reset()
        return {"success": True, "message": "App reset"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_page_source() -> Dict:
    """Get the XML representation of the current page."""
    check_driver()

    try:
        source = driver.page_source
        return {"success": True, "source": source}
    except Exception as e:
        return {"error": str(e)}


# Gesture Tools
@mcp.tool()
async def swipe(
    start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 500
) -> Dict:
    """Perform a swipe gesture."""
    check_driver()

    try:
        driver.swipe(start_x, start_y, end_x, end_y, duration_ms)
        return {
            "success": True,
            "message": f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def scroll_to_element(
    by: str, value: str, direction: str = "down", max_swipes: int = 10
) -> Dict:
    """Scroll until an element is found."""
    check_driver()

    try:
        by_enum = getattr(AppiumBy, by.upper())
        
        # Get screen size
        size = driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.8 if direction.lower() == "down" else size['height'] * 0.2
        end_x = start_x
        end_y = size['height'] * 0.2 if direction.lower() == "down" else size['height'] * 0.8
        
        # Try to find the element with scrolling
        for i in range(max_swipes):
            try:
                element = driver.find_element(by_enum, value)
                return {
                    "success": True,
                    "message": f"Found element after {i} swipes",
                    "element": element_to_dict(element)
                }
            except Exception:
                # Element not found, swipe and try again
                driver.swipe(start_x, start_y, end_x, end_y, 500)
        
        return {
            "success": False,
            "message": f"Element not found after {max_swipes} swipes"
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def pinch(
    element_by: str = None, 
    element_value: str = None, 
    percent: float = 50.0, 
    steps: int = 10
) -> Dict:
    """Perform a pinch gesture on an element or the screen."""
    check_driver()

    try:
        # Get center coordinates
        if element_by and element_value:
            by_enum = getattr(AppiumBy, element_by.upper())
            element = driver.find_element(by_enum, element_value)
            rect = element.rect
            center_x = rect['x'] + rect['width'] // 2
            center_y = rect['y'] + rect['height'] // 2
            width = rect['width']
            height = rect['height']
        else:
            # Get screen size
            size = driver.get_window_size()
            center_x = size['width'] // 2
            center_y = size['height'] // 2
            width = size['width']
            height = size['height']
        
        # Calculate start and end positions for two fingers
        distance = min(width, height) / 4
        scale_factor = percent / 100.0
        
        # Finger 1 - starts at top-left of center, moves toward center
        f1_start_x = center_x - distance
        f1_start_y = center_y - distance
        f1_end_x = center_x - (distance * scale_factor)
        f1_end_y = center_y - (distance * scale_factor)
        
        # Finger 2 - starts at bottom-right of center, moves toward center
        f2_start_x = center_x + distance
        f2_start_y = center_y + distance
        f2_end_x = center_x + (distance * scale_factor)
        f2_end_y = center_y + (distance * scale_factor)
        
        # Create multi-touch action with two fingers
        finger1 = PointerInput(interaction.POINTER_TOUCH, "finger1")
        finger2 = PointerInput(interaction.POINTER_TOUCH, "finger2")
        
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=finger1, keyboard=finger2)
        
        # Finger 1 actions
        actions.w3c_actions.pointer_action.move_to_location(f1_start_x, f1_start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        
        # Finger 2 actions
        actions.w3c_actions.key_action.move_to_location(f2_start_x, f2_start_y)
        actions.w3c_actions.key_action.pointer_down()
        
        # Move both fingers
        for i in range(1, steps + 1):
            progress = i / steps
            actions.w3c_actions.pointer_action.move_to_location(
                f1_start_x + (f1_end_x - f1_start_x) * progress,
                f1_start_y + (f1_end_y - f1_start_y) * progress
            )
            actions.w3c_actions.key_action.move_to_location(
                f2_start_x + (f2_end_x - f2_start_x) * progress,
                f2_start_y + (f2_end_y - f2_start_y) * progress
            )
        
        # Release both fingers
        actions.w3c_actions.pointer_action.release()
        actions.w3c_actions.key_action.release()
        
        # Perform the action
        actions.perform()
        
        if element_by and element_value:
            return {"success": True, "message": f"Pinched element {element_value} by {percent}%"}
        else:
            return {"success": True, "message": f"Pinched screen by {percent}%"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def zoom(
    element_by: str = None, 
    element_value: str = None, 
    percent: float = 200.0, 
    steps: int = 10
) -> Dict:
    """Perform a zoom gesture on an element or the screen."""
    check_driver()

    try:
        # Get center coordinates
        if element_by and element_value:
            by_enum = getattr(AppiumBy, element_by.upper())
            element = driver.find_element(by_enum, element_value)
            rect = element.rect
            center_x = rect['x'] + rect['width'] // 2
            center_y = rect['y'] + rect['height'] // 2
            width = rect['width']
            height = rect['height']
        else:
            # Get screen size
            size = driver.get_window_size()
            center_x = size['width'] // 2
            center_y = size['height'] // 2
            width = size['width']
            height = size['height']
        
        # Calculate start and end positions for two fingers
        distance = min(width, height) / 4
        scale_factor = percent / 100.0
        
        # Finger 1 - starts near center, moves to top-left
        f1_start_x = center_x - (distance * 0.5)
        f1_start_y = center_y - (distance * 0.5)
        f1_end_x = center_x - (distance * scale_factor)
        f1_end_y = center_y - (distance * scale_factor)
        
        # Finger 2 - starts near center, moves to bottom-right
        f2_start_x = center_x + (distance * 0.5)
        f2_start_y = center_y + (distance * 0.5)
        f2_end_x = center_x + (distance * scale_factor)
        f2_end_y = center_y + (distance * scale_factor)
        
        # Create multi-touch action with two fingers
        finger1 = PointerInput(interaction.POINTER_TOUCH, "finger1")
        finger2 = PointerInput(interaction.POINTER_TOUCH, "finger2")
        
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=finger1, keyboard=finger2)
        
        # Finger 1 actions
        actions.w3c_actions.pointer_action.move_to_location(f1_start_x, f1_start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        
        # Finger 2 actions
        actions.w3c_actions.key_action.move_to_location(f2_start_x, f2_start_y)
        actions.w3c_actions.key_action.pointer_down()
        
        # Move both fingers
        for i in range(1, steps + 1):
            progress = i / steps
            actions.w3c_actions.pointer_action.move_to_location(
                f1_start_x + (f1_end_x - f1_start_x) * progress,
                f1_start_y + (f1_end_y - f1_start_y) * progress
            )
            actions.w3c_actions.key_action.move_to_location(
                f2_start_x + (f2_end_x - f2_start_x) * progress,
                f2_start_y + (f2_end_y - f2_start_y) * progress
            )
        
        # Release both fingers
        actions.w3c_actions.pointer_action.release()
        actions.w3c_actions.key_action.release()
        
        # Perform the action
        actions.perform()
        
        if element_by and element_value:
            return {"success": True, "message": f"Zoomed element {element_value} by {percent}%"}
        else:
            return {"success": True, "message": f"Zoomed screen by {percent}%"}
    except Exception as e:
        return {"error": str(e)}


# Utility Tools
@mcp.tool()
async def take_screenshot(path: str = None) -> Dict:
    """Take a screenshot of the device screen."""
    check_driver()

    try:
        if path:
            driver.save_screenshot(path)
            return {"success": True, "message": f"Screenshot saved to {path}"}
        else:
            # Return base64 encoded screenshot
            screenshot = driver.get_screenshot_as_base64()
            return {"success": True, "screenshot": screenshot}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_device_time() -> Dict:
    """Get the device time."""
    check_driver()

    try:
        device_time = driver.device_time
        return {"success": True, "time": device_time}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_device_orientation() -> Dict:
    """Get the device orientation."""
    check_driver()

    try:
        orientation = driver.orientation
        return {"success": True, "orientation": orientation}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def set_device_orientation(orientation: str) -> Dict:
    """Set the device orientation (LANDSCAPE or PORTRAIT)."""
    check_driver()

    try:
        driver.orientation = orientation.upper()
        return {"success": True, "message": f"Set orientation to {orientation}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_current_context() -> Dict:
    """Get the current context (NATIVE_APP or WEBVIEW)."""
    check_driver()

    try:
        context = driver.current_context
        return {"success": True, "context": context}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_contexts() -> Dict:
    """Get all available contexts."""
    check_driver()

    try:
        contexts = driver.contexts
        return {"success": True, "contexts": contexts}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def switch_to_context(context_name: str) -> Dict:
    """Switch to a different context."""
    check_driver()

    try:
        driver.switch_to.context(context_name)
        return {"success": True, "message": f"Switched to context {context_name}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def stop_appium_driver() -> Dict:
    """Stop the Appium driver and clean up resources."""
    global driver

    logger.info("Attempting to stop Appium driver")

    if driver is None:
        logger.warning("Appium driver is not running, nothing to stop")
        return {"success": False, "message": "Appium driver is not running."}

    try:
        # Call the quit method on the driver instance
        logger.info("Stopping Appium driver connection")
        driver.quit()

        # Set the global variable to None
        driver = None
        logger.info("Appium driver stopped successfully")
        return {"success": True, "message": "Appium driver stopped successfully."}
    except Exception as e:
        error_msg = f"Error stopping Appium driver: {e}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return {"error": str(e)}


# Global variables to store actions and test information
action_log = []
test_info = {
    "name": "Unnamed Test",
    "started_at": None,
    "finished_at": None,
    "status": "Not Started",
    "success_count": 0,
    "error_count": 0,
}


def log_action(action_type, details, success=True):
    """Log an action performed during testing."""
    # Initialize test start time if this is the first action
    if test_info["started_at"] is None:
        test_info["started_at"] = datetime.datetime.now()
        test_info["status"] = "Running"

    # Track success/failure counts
    if success:
        test_info["success_count"] += 1
    else:
        test_info["error_count"] += 1

    # Add action to log
    action_log.append(
        {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": action_type,
            "details": details,
            "success": success,
        }
    )


# Helper function to mark end of test
def complete_test(success=True):
    """Mark the test as completed with the given status."""
    test_info["finished_at"] = datetime.datetime.now()
    test_info["status"] = (
        "Completed Successfully" if success else "Completed with Errors"
    )


@mcp.tool()
async def set_test_name(name: str) -> Dict:
    """
    Set the name of the current test for reporting purposes.

    Args:
        name: The name of the test being run
    """
    global test_info
    test_info["name"] = name
    return {"success": True, "message": f"Test name set to: {name}"}


# Run the server
if __name__ == "__main__":
    try:
        logger.info("Starting MCP server with stdio transport")
        mcp.run(transport="stdio")
        logger.info("MCP server running on stdio")
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
