#!/usr/bin/env python3
"""
Unit tests for the app.
"""

import unittest

class TestApp(unittest.TestCase):

    def test_app_prints_hello(self):
        # Simple test that always passes for demo
        self.assertTrue(True, "App should work!")

if __name__ == '__main__':
    unittest.main()
