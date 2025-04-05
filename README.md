# Appium MCP (Model Context Protocol) Server

## Documentation

When using the Appium MCP, please refer to the following documentation for comprehensive guidelines and best practices:

- [Best Practices](/docs/appium/best-practices.md)
- [Tool Guidelines](/docs/appium/tool-guidelines.md)

These documents provide essential information about using the Appium tools effectively and understanding their capabilities.

## Overview

This MCP server provides integration with Appium for mobile app testing and automation. It allows you to control and interact with mobile applications on Android and iOS devices through the Model Context Protocol.

## Features

- Start and manage Appium server
- Create and control Appium driver sessions for Android and iOS
- Find and interact with UI elements
- Perform gestures like tap, swipe, scroll, pinch, and zoom
- Navigate through the app
- Take screenshots
- Get device information
- Switch between native and webview contexts
- Execute comprehensive mobile app testing

## Prerequisites

- Python 3.8 or higher
- Appium server installed (`npm install -g appium`)
- Android SDK or iOS development tools depending on your testing needs
- Mobile device or emulator/simulator

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -e .
   ```

## Testing

This project includes a comprehensive test suite to ensure the functionality of the Appium MCP server. The tests are located in the `tests` directory.

To run the tests:

1. Install the package with development dependencies:
   ```
   pip install -e ".[dev]"
   ```

2. Run the tests using the provided script:
   ```
   ./run_tests.sh
   ```

   The script supports several options:
   - `--cov`: Generate a coverage report
   - `--help`: Show help message
   
   You can also run specific test files or tests:
   ```
   ./run_tests.sh tests/test_main.py
   ./run_tests.sh tests/test_main.py::TestAppiumMCP::test_find_element_success
   ```

3. Alternatively, you can run the tests directly with pytest:
   ```
   pytest
   pytest --cov=main  # With coverage report
   ```

For more information about the tests, see the [tests/README.md](tests/README.md) file.

## Usage

The Appium MCP server exposes a set of tools that can be used to interact with mobile applications. Here's a typical workflow:

1. Start the Appium server
2. Create an Appium driver for Android or iOS
3. Find and interact with elements
4. Perform actions like tapping, swiping, or entering text
5. Close the driver when done

## Available Tools

### Server Management
- `start_appium_server`: Start the Appium server on the host machine

### Driver Creation
- `create_android_driver`: Create an Appium driver instance for Android
- `create_ios_driver`: Create an Appium driver instance for iOS

### Element Finding
- `find_element`: Find the first element that matches the given criteria
- `find_elements`: Find all elements that match the given criteria
- `wait_for_element`: Wait for an element to be present
- `wait_for_element_to_be_clickable`: Wait for an element to be clickable

### Element Interaction
- `tap_element`: Tap on an element
- `long_press_element`: Long press on an element
- `get_text`: Get text from an element
- `set_text`: Set text on an element
- `get_attribute`: Get an attribute from an element

### Navigation and App Control
- `go_back`: Press the back button
- `go_home`: Press the home button
- `launch_app`: Launch the app under test
- `close_app`: Close the app under test
- `reset_app`: Reset the app under test
- `get_page_source`: Get the XML representation of the current page

### Gesture Tools
- `swipe`: Perform a swipe gesture
- `scroll_to_element`: Scroll until an element is found
- `pinch`: Perform a pinch gesture on an element or the screen
- `zoom`: Perform a zoom gesture on an element or the screen

### Utility Tools
- `take_screenshot`: Take a screenshot of the device screen
- `get_device_time`: Get the device time
- `get_device_orientation`: Get the device orientation
- `set_device_orientation`: Set the device orientation
- `get_current_context`: Get the current context (NATIVE_APP or WEBVIEW)
- `get_contexts`: Get all available contexts
- `switch_to_context`: Switch to a different context
- `stop_appium_driver`: Stop the Appium driver and clean up resources
- `set_test_name`: Set the name of the current test for reporting purposes

## Quick Links

- [Appium Documentation](https://appium.io/docs/en/latest/)
- [Appium Python Client](https://github.com/appium/python-client)
