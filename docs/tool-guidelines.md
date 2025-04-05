# Appium MCP Tool Guidelines

This document provides detailed information about each tool available in the Appium MCP server.

## Server Management

### start_appium_server

Starts the Appium server on the host machine.

**Parameters:** None

**Returns:** A string indicating success or failure

**Example:**
```python
result = start_appium_server()
```

**Notes:**
- Ensure Appium is installed on your system (`npm install -g appium`)
- The server runs on the default port 4723
- This must be called before creating a driver

## Driver Creation

### create_android_driver

Creates an Appium driver instance for Android.

**Parameters:**
- `app_path` (optional): Path to the .apk file
- `device_name` (default: "Android Emulator"): Name of the device
- `platform_version` (default: "10.0"): Android version
- `app_package` (optional): Package name of the app
- `app_activity` (optional): Activity name to launch
- `automation_name` (default: "UiAutomator2"): Automation engine to use
- `appium_server_url` (default: "http://localhost:4723/wd/hub"): URL of the Appium server
- `no_reset` (default: false): Whether to preserve app state between sessions
- `full_reset` (default: false): Whether to uninstall app before and after test
- `auto_grant_permissions` (default: true): Whether to automatically grant app permissions

**Returns:** A string indicating success or failure

**Example:**
```python
result = create_android_driver(
    app_path="/path/to/app.apk",
    device_name="Pixel 4",
    platform_version="11.0"
)
```

**Notes:**
- Either `app_path` or both `app_package` and `app_activity` must be provided
- For testing an installed app, use `app_package` and `app_activity`
- For testing a new app, use `app_path`

### create_ios_driver

Creates an Appium driver instance for iOS.

**Parameters:**
- `app_path` (optional): Path to the .app or .ipa file
- `device_name` (default: "iPhone Simulator"): Name of the device
- `platform_version` (default: "15.0"): iOS version
- `bundle_id` (optional): Bundle ID of the app
- `automation_name` (default: "XCUITest"): Automation engine to use
- `appium_server_url` (default: "http://localhost:4723/wd/hub"): URL of the Appium server
- `no_reset` (default: false): Whether to preserve app state between sessions
- `full_reset` (default: false): Whether to uninstall app before and after test
- `auto_accept_alerts` (default: true): Whether to automatically accept alerts

**Returns:** A string indicating success or failure

**Example:**
```python
result = create_ios_driver(
    app_path="/path/to/app.app",
    device_name="iPhone 13",
    platform_version="15.4"
)
```

**Notes:**
- Either `app_path` or `bundle_id` must be provided
- For testing an installed app, use `bundle_id`
- For testing a new app, use `app_path`

## Element Finding

### find_element

Finds the first element that matches the given criteria.

**Parameters:**
- `by`: Locator strategy (ID, ACCESSIBILITY_ID, CLASS_NAME, NAME, XPATH, etc.)
- `value`: Value to search for
- `timeout` (default: 10.0): Maximum time to wait for the element in seconds

**Returns:** A dictionary containing element details or an error

**Example:**
```python
element = find_element(by="ID", value="login_button")
```

### find_elements

Finds all elements that match the given criteria.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `timeout` (default: 10.0): Maximum time to wait for at least one element in seconds

**Returns:** A list of dictionaries containing element details or an error

**Example:**
```python
elements = find_elements(by="CLASS_NAME", value="android.widget.Button")
```

### wait_for_element

Waits for an element to be present.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `timeout` (default: 20.0): Maximum time to wait in seconds

**Returns:** A dictionary containing element details or an error

**Example:**
```python
element = wait_for_element(by="ID", value="results", timeout=30.0)
```

### wait_for_element_to_be_clickable

Waits for an element to be clickable.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `timeout` (default: 20.0): Maximum time to wait in seconds

**Returns:** A dictionary containing element details or an error

**Example:**
```python
element = wait_for_element_to_be_clickable(by="ID", value="submit_button")
```

## Element Interaction

### tap_element

Taps on an element.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `timeout` (default: 10.0): Maximum time to wait for the element in seconds

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = tap_element(by="ID", value="login_button")
```

### long_press_element

Long presses on an element.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `duration_ms` (default: 1000): Duration of the long press in milliseconds
- `timeout` (default: 10.0): Maximum time to wait for the element in seconds

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = long_press_element(by="ID", value="item", duration_ms=2000)
```

### get_text

Gets text from an element.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `timeout` (default: 10.0): Maximum time to wait for the element in seconds

**Returns:** A dictionary containing the text or an error

**Example:**
```python
result = get_text(by="ID", value="message")
text = result["text"]
```

### set_text

Sets text on an element.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `text`: Text to set
- `clear_first` (default: true): Whether to clear the field before setting text
- `timeout` (default: 10.0): Maximum time to wait for the element in seconds

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = set_text(by="ID", value="username", text="testuser")
```

### get_attribute

Gets an attribute from an element.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `attribute`: Name of the attribute to get
- `timeout` (default: 10.0): Maximum time to wait for the element in seconds

**Returns:** A dictionary containing the attribute value or an error

**Example:**
```python
result = get_attribute(by="ID", value="status", attribute="checked")
is_checked = result["value"]
```

## Navigation and App Control

### go_back

Presses the back button.

**Parameters:** None

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = go_back()
```

### go_home

Presses the home button.

**Parameters:** None

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = go_home()
```

### launch_app

Launches the app under test.

**Parameters:** None

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = launch_app()
```

### close_app

Closes the app under test.

**Parameters:** None

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = close_app()
```

### reset_app

Resets the app under test.

**Parameters:** None

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = reset_app()
```

### get_page_source

Gets the XML representation of the current page.

**Parameters:** None

**Returns:** A dictionary containing the page source or an error

**Example:**
```python
result = get_page_source()
source = result["source"]
```

## Gesture Tools

### swipe

Performs a swipe gesture.

**Parameters:**
- `start_x`: Starting X coordinate
- `start_y`: Starting Y coordinate
- `end_x`: Ending X coordinate
- `end_y`: Ending Y coordinate
- `duration_ms` (default: 500): Duration of the swipe in milliseconds

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = swipe(start_x=100, start_y=500, end_x=100, end_y=200)
```

### scroll_to_element

Scrolls until an element is found.

**Parameters:**
- `by`: Locator strategy
- `value`: Value to search for
- `direction` (default: "down"): Direction to scroll ("up" or "down")
- `max_swipes` (default: 10): Maximum number of swipes to perform

**Returns:** A dictionary containing the element or an error

**Example:**
```python
result = scroll_to_element(by="TEXT", value="Settings", direction="down")
```

### pinch

Performs a pinch gesture on an element or the screen.

**Parameters:**
- `element_by` (optional): Locator strategy for the element
- `element_value` (optional): Value to search for
- `percent` (default: 50.0): Percentage to pinch (smaller values = pinch more)
- `steps` (default: 10): Number of steps in the gesture

**Returns:** A dictionary indicating success or an error

**Example:**
```python
# Pinch on an element
result = pinch(element_by="ID", element_value="image", percent=40.0)

# Pinch on the screen
result = pinch(percent=50.0)
```

### zoom

Performs a zoom gesture on an element or the screen.

**Parameters:**
- `element_by` (optional): Locator strategy for the element
- `element_value` (optional): Value to search for
- `percent` (default: 200.0): Percentage to zoom (larger values = zoom more)
- `steps` (default: 10): Number of steps in the gesture

**Returns:** A dictionary indicating success or an error

**Example:**
```python
# Zoom on an element
result = zoom(element_by="ID", element_value="image", percent=250.0)

# Zoom on the screen
result = zoom(percent=200.0)
```

## Utility Tools

### take_screenshot

Takes a screenshot of the device screen.

**Parameters:**
- `path` (optional): Path to save the screenshot

**Returns:** A dictionary containing the screenshot as base64 or a success message

**Example:**
```python
# Save to file
result = take_screenshot(path="/path/to/screenshot.png")

# Get base64 data
result = take_screenshot()
screenshot_data = result["screenshot"]
```

### get_device_time

Gets the device time.

**Parameters:** None

**Returns:** A dictionary containing the device time or an error

**Example:**
```python
result = get_device_time()
device_time = result["time"]
```

### get_device_orientation

Gets the device orientation.

**Parameters:** None

**Returns:** A dictionary containing the orientation or an error

**Example:**
```python
result = get_device_orientation()
orientation = result["orientation"]
```

### set_device_orientation

Sets the device orientation.

**Parameters:**
- `orientation`: Orientation to set ("LANDSCAPE" or "PORTRAIT")

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = set_device_orientation(orientation="LANDSCAPE")
```

### get_current_context

Gets the current context (NATIVE_APP or WEBVIEW).

**Parameters:** None

**Returns:** A dictionary containing the context or an error

**Example:**
```python
result = get_current_context()
context = result["context"]
```

### get_contexts

Gets all available contexts.

**Parameters:** None

**Returns:** A dictionary containing the available contexts or an error

**Example:**
```python
result = get_contexts()
contexts = result["contexts"]
```

### switch_to_context

Switches to a different context.

**Parameters:**
- `context_name`: Name of the context to switch to

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = switch_to_context(context_name="WEBVIEW_1")
```

### stop_appium_driver

Stops the Appium driver and cleans up resources.

**Parameters:** None

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = stop_appium_driver()
```

### set_test_name

Sets the name of the current test for reporting purposes.

**Parameters:**
- `name`: Name of the test

**Returns:** A dictionary indicating success or an error

**Example:**
```python
result = set_test_name(name="Login Test")
```
