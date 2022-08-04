import unittest
import json
import os

from .utils import zotero_description

file_path = os.path.dirname(os.path.realpath(__file__))
fixtures_path = os.path.join(file_path, 'fixtures')

with open(os.path.join(fixtures_path, "zotero.json")) as f:
    zotero_data = json.load(f)


class TestUtilityFunctions(unittest.TestCase):

    def test_zotero_description(self):
        item_data = zotero_data[0]['data']
        data = zotero_description(item_data)
        print(data)
        self.assertEqual(data['id'], '#frd_bibl_V9N337QB')
        self.assertTrue(data['value'].startswith('Studien über Hysterie'))
