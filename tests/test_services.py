import unittest

from worldview.core.services import get_domain_summary, get_providers, get_required_keys


class ServicesTestCase(unittest.TestCase):
    def test_provider_registry_has_entries(self):
        providers = get_providers()
        self.assertGreater(len(providers), 50)

    def test_required_keys_non_empty(self):
        keys = get_required_keys()
        self.assertIn("OPENSKY_CLIENT_ID", keys)

    def test_domain_summary_has_counts(self):
        summary = get_domain_summary()
        self.assertGreater(len(summary), 5)
        self.assertTrue(all(item["total"] >= item["free_tier"] for item in summary))


if __name__ == "__main__":
    unittest.main()
