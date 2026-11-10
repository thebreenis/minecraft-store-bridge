import unittest
import account_guard as guard

class AccountTests(unittest.TestCase):
    def test_missing_display_name_does_not_block(self):
        a=guard.Accounts("same","123","","same","")
        self.assertEqual(guard.decision(a),"reauth")
        self.assertEqual(guard.decision(a,"123"),"ready")
        self.assertEqual(guard.decision(a,"456"),"reauth")
        self.assertIn("Gamertag unavailable",guard.describe(a))
    def test_windows_mismatch(self):
        a=guard.Accounts("one","123","Same","two","Same")
        self.assertEqual(guard.decision(a,"123"),"windows_mismatch")
    def test_missing_ids(self):
        for a in (guard.Accounts(),guard.Accounts("same","","Name","same","Name"),guard.Accounts("same","123","Name","","")):
            self.assertEqual(guard.decision(a,"123"),"unverified")
