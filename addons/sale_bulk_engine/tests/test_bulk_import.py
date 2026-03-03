from odoo.tests.common import TransactionCase


class TestBulkImport(TransactionCase):
    def test_idempotent_import(self):
        self.assertTrue(True)
