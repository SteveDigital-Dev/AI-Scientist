import unittest


class FailureFixtureTest(unittest.TestCase):
    def test_expected_failure_signal(self):
        self.assertEqual("baseline", "candidate")

