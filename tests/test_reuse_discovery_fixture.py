import unittest


class ReuseDiscoveryFixtureTest(unittest.TestCase):
    """Fails on trial reuse unless the discovered suite is cloned per run."""

    def test_state_does_not_leak_between_trials(self):
        self.assertFalse(hasattr(self, "_seen"))
        self._seen = True


if __name__ == "__main__":
    unittest.main()
