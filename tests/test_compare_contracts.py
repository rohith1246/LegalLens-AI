"""
Tests for Pillar 2: Compare Contracts (Contract Redliner & Diff Engine).
Verifies semantic intent diffing, favorable/unfavorable rating, and risk delta.
"""

import unittest
import json
from app import app
from sample_contracts import SAMPLE_CONTRACTS
from contract_comparator import comparator_engine


class CompareContractsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.text_a = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        self.text_b = SAMPLE_CONTRACTS["msa_comparison_v2"]["text"]

    def test_compare_versions_unit(self):
        """Unit test: compare baseline against counterparty redline markup."""
        res = comparator_engine.compare_contracts(self.text_a, self.text_b)
        
        self.assertIn("net_risk_delta", res)
        self.assertIn("score_delta", res)
        self.assertIn("clause_changes", res)
        self.assertIn("negotiation_verdict", res)
        self.assertEqual(res["net_risk_delta"], "Significantly Favorable")

    def test_detect_semantic_shifts(self):
        """Verify semantic shift detection across contract clauses."""
        shifts = comparator_engine.detect_semantic_shifts(self.text_a, self.text_b)
        self.assertGreaterEqual(len(shifts), 2)
        for shift in shifts:
            self.assertIn("section_title", shift)
            self.assertIn("impact", shift)
            self.assertIn("analysis", shift)

    def test_calculate_risk_delta(self):
        """Verify risk delta calculation and verdict."""
        delta = comparator_engine.calculate_risk_delta(self.text_a, self.text_b)
        self.assertEqual(delta["net_risk_delta"], "Significantly Favorable")
        self.assertIn("+34", delta["score_delta"])

    def test_api_route_compare_contracts(self):
        """Verify dedicated /api/compare-contracts endpoint."""
        res = self.app.post("/api/compare-contracts",
                            data=json.dumps({"text_a": self.text_a, "text_b": self.text_b}),
                            content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("net_risk_delta", data)


if __name__ == "__main__":
    unittest.main()
