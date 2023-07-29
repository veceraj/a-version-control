"""Test Suite Module"""

import unittest
from tests.test_scenario_1 import TestScenario1

# from tests.test_scenario_2 import TestScenario2
# from tests.test_scenario_3 import TestScenario3


def get_suite():
    """Define a test suite"""
    suite = unittest.TestSuite()
    suite.addTest(TestScenario1())
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(get_suite())
