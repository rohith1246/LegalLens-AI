"""
Tests for Pillar 1: Simplify Complex Legal Docs.
Verifies plain-English translation, health scores, rights vs obligations, and red flags.
"""

import unittest
import json
from app import app
from sample_contracts import SAMPLE_CONTRACTS
from legal_simplifier import simplifier_engine


class SimplifyLegalDocsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_simplify_freelance_msa(self):
        """Verify complete simplification of Freelance Master Services Agreement."""
        text = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        result = simplifier_engine.simplify_document(text)
        
        self.assertIn("overall_health_score", result)
        self.assertIn("risk_tier", result)
        self.assertIn("executive_summary", result)
        self.assertIn("layman_eli5", result)
        self.assertIn("red_flags", result)
        self.assertIn("rights_and_obligations", result)
        self.assertGreaterEqual(len(result["red_flags"]), 1)

    def test_extract_rights_and_obligations(self):
        """Verify 3-column rights vs obligations extraction."""
        text = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        ro = simplifier_engine.extract_rights_and_obligations(text)
        
        self.assertIn("your_rights", ro)
        self.assertIn("your_obligations", ro)
        self.assertIn("counterparty_obligations", ro)
        self.assertGreaterEqual(len(ro["your_rights"]), 1)

    def test_audit_risk_radar(self):
        """Verify risk radar returns health score and categorized vulnerabilities."""
        text = SAMPLE_CONTRACTS["residential_lease"]["text"]
        radar = simplifier_engine.audit_risk_radar(text)
        
        self.assertIn("health_score", radar)
        self.assertEqual(radar["health_score"], 38)
        self.assertEqual(radar["risk_tier"], "High Risk")
        self.assertGreaterEqual(len(radar["red_flags"]), 2)

    def test_api_route_simplify_legal_docs(self):
        """Verify dedicated /api/simplify-legal-docs endpoint."""
        text = SAMPLE_CONTRACTS["saas_tos"]["text"]
        res = self.app.post("/api/simplify-legal-docs",
                            data=json.dumps({"text": text}),
                            content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["overall_health_score"], 42)


if __name__ == "__main__":
    unittest.main()
