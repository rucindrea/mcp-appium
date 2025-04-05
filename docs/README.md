# Appium MCP Documentation

This directory contains documentation for the Appium MCP server.

## Contents

- [Best Practices](best-practices.md): Guidelines for effectively using the Appium MCP server
- [Tool Guidelines](tool-guidelines.md): Detailed information about each tool provided by the Appium MCP server

## External Resources

- [Appium Documentation](https://appium.io/docs/en/latest/)
- [Appium Python Client Documentation](https://github.com/appium/python-client)
- [Selenium Python Documentation](https://selenium-python.readthedocs.io/)

## Getting Started

To get started with the Appium MCP server, you'll need:

1. Appium installed on your system
2. A mobile device or emulator/simulator
3. The appropriate mobile app for testing

Follow these steps:

1. Start the Appium server using the `start_appium_server` tool
2. Create a driver session using either `create_android_driver` or `create_ios_driver`
3. Use the various tools to interact with your mobile application
4. When finished, use `stop_appium_driver` to clean up resources

## Common Usage Patterns

### Finding Elements

Elements can be found using various locator strategies:

- ID
- ACCESSIBILITY_ID
- CLASS_NAME
- NAME
- XPATH
- CSS_SELECTOR (for webview contexts)

Example:
```python
element = find_element(by="ID", value="login_button")
```

### Interacting with Elements

Once you've found an element, you can interact with it:

```python
# Tap on an element
tap_element(by="ID", value="login_button")

# Enter text
set_text(by="ID", value="username_field", text="testuser")
```

### Gestures

Perform common mobile gestures:

```python
# Swipe from one point to another
swipe(start_x=100, start_y=500, end_x=100, end_y=200)

# Scroll until an element is found
scroll_to_element(by="TEXT", value="Settings")
```
