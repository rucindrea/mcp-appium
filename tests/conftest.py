"""
Configuration file for pytest.
This file is automatically loaded by pytest and can contain fixtures and other setup code.
"""
import os
import sys

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
