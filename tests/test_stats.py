import unittest
from analytics import stats
from datetime import datetime

class TestStats(unittest.TestCase):
    def test_get_stats_no_data(self):
        # Test: Keine Daten vorhanden, sollte leere oder Standardwerte liefern
        result = stats.get_stats()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], str)

    def test_get_leaderboards_no_data(self):
        # Test: Keine Daten vorhanden, sollte leere Listen liefern
        kill_lb, death_lb = stats.get_leaderboards()
        self.assertIsInstance(kill_lb, list)
        self.assertIsInstance(death_lb, list)

    def test_get_recent_kill_events_no_data(self):
        # Test: Keine Daten vorhanden, sollte leeren String liefern
        recent = stats.get_recent_kill_events()
        self.assertIsInstance(recent, str)

if __name__ == '__main__':
    unittest.main()
