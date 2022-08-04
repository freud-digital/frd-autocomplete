import unittest
import json
import os

from .utils import zotero_description, populate_baserow_response, populate_zotero_response

file_path = os.path.dirname(os.path.realpath(__file__))
fixtures_path = os.path.join(file_path, 'fixtures')

with open(os.path.join(fixtures_path, "zotero.json")) as f:
    zotero_data = json.load(f)

with open(os.path.join(fixtures_path, "baserow.json")) as f:
    baserow_data = json.load(f)


class TestUtilityFunctions(unittest.TestCase):

    def test_zotero_description(self):
        item_data = zotero_data[0]['data']
        data = zotero_description(item_data)
        print(data)
        self.assertEqual(data['id'], '#frd_bibl_V9N337QB')
        self.assertTrue(data['value'].startswith('Studien über Hysterie'))

    def test_populate_zotero_response(self):
        data = populate_zotero_response(zotero_data, "select2")
        keys = data['results'][0].keys()
        self.assertIn('id', keys)
        data = populate_zotero_response(zotero_data)
        keys = data['tc:suggestion'][0].keys()
        self.assertIn('tc:description', keys)
        data = populate_zotero_response(zotero_data, format='original')
        keys = data['result'][0].keys()
        self.assertIn('key', keys)

    def test_baserow_population_select2(self):
        data = populate_baserow_response(baserow_data, format="select2")
        keys = data['results'][0].keys()
        self.assertIn('id', keys)

    def test_baserow_population_teicompleter(self):
        data = populate_baserow_response(baserow_data)
        keys = data['tc:suggestion'][0].keys()
        self.assertIn('tc:description', keys)
        self.assertTrue('tc:description', 'Freud, Sigmund')

    def test_baserow_population_original(self):
        data = populate_baserow_response(baserow_data, format='original')
        keys = data['results']['results'][0].keys()
        self.assertIn('frd_id', keys)
        self.assertTrue(data['results']['results'][0]['name'], 'Freud, Sigmund')
