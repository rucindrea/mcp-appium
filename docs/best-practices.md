# Appium MCP Best Practices

This document outlines best practices for using the Appium MCP server effectively.

## General Guidelines

1. **Initialize and Clean Up Properly**
   - Always start the Appium server before creating a driver
   - Always stop the Appium driver when you're done to release resources
   - Use try/finally blocks to ensure cleanup happens even if errors occur

2. **Use Appropriate Waiting Strategies**
   - Prefer explicit waits over implicit waits
   - Use `wait_for_element` or `wait_for_element_to_be_clickable` instead of `find_element` when elements might not be immediately available
   - Set appropriate timeout values based on your app's performance characteristics

3. **Choose the Right Locator Strategy**
   - Prefer ACCESSIBILITY_ID or ID over XPATH when possible
   - XPATH should be a last resort as it's slower and more brittle
   - Use resource-id for Android and accessibility identifiers for iOS when possible

4. **Handle Context Switching Properly**
   - When testing hybrid apps, be aware of which context you're in (NATIVE_APP or WEBVIEW)
   - Use `get_contexts` to see available contexts
   - Switch contexts using `switch_to_context` when needed

## Performance Optimization

1. **Minimize Driver Creation**
   - Creating a new driver session is expensive
   - Reuse the same driver for multiple tests when possible
   - Consider using `reset_app` instead of creating a new driver for each test

2. **Optimize Element Finding**
   - Cache element references when you'll use them multiple times
   - Use more specific locators to reduce search time
   - Limit the use of `find_elements` with broad selectors

3. **Batch Operations When Possible**
   - Group related actions together to minimize round trips
   - Consider using `execute_script` for complex operations (if available)

## Stability Improvements

1. **Handle Unexpected Alerts**
   - Set `auto_accept_alerts` or `auto_grant_permissions` to true when creating the driver
   - Have fallback mechanisms for handling unexpected popups

2. **Implement Retry Logic**
   - Mobile testing is inherently flaky
   - Implement retry mechanisms for critical operations
   - Use exponential backoff for retries

3. **Adapt to Different Screen Sizes**
   - Don't hardcode coordinates unless absolutely necessary
   - Use relative positioning based on screen size when using coordinates
   - Test on multiple device sizes if possible

## Debugging Tips

1. **Use Screenshots Liberally**
   - Take screenshots at key points in your test
   - Always capture a screenshot when an error occurs

2. **Examine Page Source**
   - Use `get_page_source` to see the current UI hierarchy
   - This can help identify why elements aren't being found

3. **Log Detailed Information**
   - Log device information at the start of tests
   - Log each action being performed
   - Include timestamps in logs

## Testing Specific Interactions

1. **Text Input**
   - Always clear fields before entering text unless you're specifically testing appending
   - Verify text was entered correctly after setting it

2. **Scrolling and Swiping**
   - Use `scroll_to_element` instead of manual swipes when looking for elements
   - For manual swipes, calculate coordinates based on screen size percentages

3. **Gestures**
   - Test complex gestures (pinch, zoom) on different device sizes
   - Be aware that gesture behavior can vary between devices

## Continuous Integration

1. **Device Management**
   - Use a device farm or emulator/simulator grid for CI
   - Ensure devices are in a clean state before tests

2. **Parallel Execution**
   - Run tests in parallel on multiple devices when possible
   - Use unique port numbers for each Appium server instance

3. **Reporting**
   - Generate detailed reports with screenshots
   - Track test execution times to identify slow tests
