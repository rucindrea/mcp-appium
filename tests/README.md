# Appium MCP Server Tests

This directory contains tests for the Appium MCP server implementation. The tests are written using pytest and cover various aspects of the server's functionality.

## Test Structure

The tests are organized into several modules:

- **test_action_logging.py**: Tests for the action logging functionality.
- **test_async_functions.py**: Tests for the async functions in the main module.
- **test_error_handling.py**: Tests for error handling in the main module.
- **test_gesture_tools.py**: Tests for the gesture tools (swipe, pinch, zoom, etc.).
- **test_main.py**: Tests for the main functionality of the Appium MCP server.
- **test_mcp_server.py**: Tests for the MCP server functionality.

## Running the Tests

To run the tests, use the following command from the root directory of the project:

```bash
python -m pytest
```

To run the tests with coverage:

```bash
python -m pytest --cov=main tests/
```

To run a specific test file:

```bash
python -m pytest tests/test_main.py
```

To run a specific test:

```bash
python -m pytest tests/test_main.py::TestAppiumMCP::test_start_appium_server_success
```

## Test Fixtures

The tests use pytest fixtures to set up and tear down test environments. These fixtures are defined in the `conftest.py` file.

## Mocking

The tests use the `unittest.mock` module to mock external dependencies, such as the Appium driver, WebDriverWait, and subprocess.Popen. This allows the tests to run without actually starting an Appium server or connecting to a device.

## Async Testing

Many of the tests are async tests, as they test async functions. These tests are marked with the `@pytest.mark.asyncio` decorator, which allows pytest to run them in an asyncio event loop.

## Error Handling

The tests for error handling check that the server properly handles exceptions and returns appropriate error messages to the client.

## Action Logging

The tests for action logging check that the server properly logs actions and maintains the test state.

## Gesture Tools

The tests for gesture tools check that the server properly implements swipe, pinch, zoom, and other gesture operations.

## MCP Server

The tests for the MCP server check that the server properly initializes and registers tools with the MCP framework.
