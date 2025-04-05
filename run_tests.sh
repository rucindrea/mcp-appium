#!/bin/bash

# Run tests for Appium MCP server
echo "Running tests for Appium MCP server..."

# Check if a specific test file or test was specified
if [ $# -eq 0 ]; then
    # No arguments, run all tests
    echo "Running command: pytest"
    python -m pytest
elif [ $# -eq 1 ] && [ "$1" == "--cov" ]; then
    # Run with coverage
    echo "Running command: pytest --cov=main tests/"
    python -m pytest --cov=main tests/
elif [ $# -eq 1 ] && [ "$1" == "--help" ]; then
    # Show help
    echo "Usage: ./run_tests.sh [options] [test_file] [test_name]"
    echo ""
    echo "Options:"
    echo "  --cov       Run tests with coverage"
    echo "  --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_tests.sh                                                  # Run all tests"
    echo "  ./run_tests.sh --cov                                            # Run all tests with coverage"
    echo "  ./run_tests.sh tests/test_main.py                               # Run tests in test_main.py"
    echo "  ./run_tests.sh tests/test_main.py::TestAppiumMCP::test_find_element_success  # Run a specific test"
    exit 0
else
    # Run specific test file or test
    echo "Running command: pytest $@"
    python -m pytest "$@"
fi

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed."
else
    echo "Some tests failed."
fi
