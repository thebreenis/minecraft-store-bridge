import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from offline_marketplace import Catalog

class SyntheticTests(unittest.TestCase):
    def setUp(self):
        self.c = Catalog()
        self.ids = list(self.c.items)
    def test_unique_legacy_identities(self):
        rows=self.c.legacy_catalog()
        self.assertEqual(rows["count"],4)
        self.assertEqual(len({r["document"]["productId"] for r in rows["results"]}),4)
    def test_free_idempotent(self):
        self.assertFalse(self.c.claim(self.ids[0])["alreadyOwned"])
        self.assertTrue(self.c.claim(self.ids[0])["alreadyOwned"])
        self.assertEqual(len(self.c.owned),1)
    def test_unknown_can_claim_not_download(self):
        self.assertEqual(self.c.action(self.ids[2])["label"],"Free")
        self.c.claim(self.ids[2])
        self.assertEqual(self.c.action(self.ids[2]),{"label":"Incompatible","enabled":False,"owned":True})
    def test_paid_and_coming_soon_rejected(self):
        for oid in (self.ids[1],self.ids[3]):
            with self.assertRaises(ValueError):self.c.claim(oid)
        self.assertFalse(self.c.owned)
    def test_missing_price_not_free(self):
        self.assertEqual(self.c.action(self.ids[3])["label"],"Coming Soon")
    def test_no_microsoft_state(self):
        self.assertIn("TAG|Synthetic Example",self.c.states())
        self.assertIn("BAL|0",self.c.states())
