import unittest
from datetime import datetime, timedelta, timezone

from worldview.core.services import (
    get_domain_summary,
    get_providers,
    get_required_keys,
    playback_telemetry,
    get_live_snapshot,
    synthesize_news_event,
    to_mgrs,
)


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

    def test_playback_filtering(self):
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=5)
        points = playback_telemetry(start_time, end_time, [-180, -90, 180, 90], ["aviation"])
        self.assertTrue(all(p["domain"] == "aviation" for p in points))

    def test_live_snapshot(self):
        points = get_live_snapshot(["marine"])
        self.assertTrue(points)
        self.assertTrue(all(p["domain"] == "marine" for p in points))

    def test_synthesis(self):
        result = synthesize_news_event(
            "https://example.com",
            "Breaking",
            "Military conflict and GPS spoofing reported near port.",
        )
        self.assertGreaterEqual(result["risk_score"], 0.7)
        self.assertIn("gnss_interference", result["entities"])

    def test_mgrs_placeholder(self):
        grid = to_mgrs(51.5, -0.12)
        self.assertIn("N", grid)


if __name__ == "__main__":
    unittest.main()
