import pytest
from unittest.mock import patch, call
import sys
import os

# Add src to path to import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from main import main

@patch('builtins.print')
def test_main_output(mock_print):
    main()
    
    # Verify the expected print calls
    expected_calls = [
        call("Hello, World!"),
        call("Welcome to oneCreditCard!")
    ]
    mock_print.assert_has_calls(expected_calls)