import unittest

# Load test modules
from unit_test import TestImageCompressor
from integration_test import TestImageCompressorIntegration
from performance_test import TestImageCompressorPerformance
from edge_case_test import TestImageCompressorEdgeCases

def run_all_tests():
    """ Runs all test cases and reports results. """
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestImageCompressor))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestImageCompressorIntegration))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestImageCompressorPerformance))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestImageCompressorEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\nAll tests passed successfully! ✅")
    else:
        print("\nSome tests failed. ❌")

if __name__ == "__main__":
    run_all_tests()
