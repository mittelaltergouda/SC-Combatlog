import unittest
from core.filter_service import FilterService
from datetime import datetime

class TestFilterService(unittest.TestCase):
    def test_build_entity_filter_dict_bool(self):
        filters = {'players': True, 'npc_pirate': False}
        result = FilterService.build_entity_filter_dict(filters)
        self.assertEqual(result, {'players': True, 'npc_pirate': False})

    def test_build_entity_filter_dict_tkvar(self):
        class DummyVar:
            def __init__(self, v): self._v = v
            def get(self): return self._v
        filters = {'players': DummyVar(True), 'npc_pirate': DummyVar(False)}
        result = FilterService.build_entity_filter_dict(filters)
        self.assertEqual(result, {'players': True, 'npc_pirate': False})

    def test_validate_date_valid(self):
        date = FilterService.validate_date('2024-05-08')
        self.assertIsInstance(date, datetime)
        self.assertEqual(date.year, 2024)
        self.assertEqual(date.month, 5)
        self.assertEqual(date.day, 8)

    def test_validate_date_empty(self):
        self.assertIsNone(FilterService.validate_date(''))

    def test_validate_date_invalid(self):
        with self.assertRaises(ValueError):
            FilterService.validate_date('08.05.2024')

    def test_is_entity_selected(self):
        filters = {'players': True, 'npc_pirate': False}
        self.assertTrue(FilterService.is_entity_selected(filters, 'players'))
        self.assertFalse(FilterService.is_entity_selected(filters, 'npc_pirate'))
        self.assertFalse(FilterService.is_entity_selected(filters, 'unknown'))

if __name__ == '__main__':
    unittest.main()
