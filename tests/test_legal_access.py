"""
Tests for Core Theme: AI for Legal Assistance & Access.
Verifies multilingual translation, localized glossaries, and comprehensive audit report generation.
"""

import unittest
import json
from app import app
from legal_access import legal_access_engine


class LegalAccessTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_translate_to_hindi(self):
        """Verify translation to Hindi with plain-language explanation and glossary."""
        text = "Contractor agrees to indemnify Client against all claims without limitation of liability."
        res = legal_access_engine.translate_to_regional_language(text, target_language="Hindi")
        
        self.assertEqual(res["target_language"], "Hindi")
        self.assertIn("translated_title", res)
        self.assertIn("plain_explanation_target_lang", res)
        self.assertIn("key_terms_glossary", res)
        self.assertGreaterEqual(len(res["key_terms_glossary"]), 1)

    def test_translate_to_spanish(self):
        """Verify translation to Spanish."""
        text = "Net-60 payment terms with 50% milestone penalty."
        res = legal_access_engine.translate_to_regional_language(text, target_language="Spanish")
        
        self.assertEqual(res["target_language"], "Spanish")
        self.assertIn("translated_content", res)

    def test_generate_legal_audit_report(self):
        """Verify comprehensive Markdown legal audit report generation."""
        mock_analysis = {
            "overall_health_score": 48,
            "risk_tier": "High Risk",
            "executive_summary": "Test executive summary",
            "layman_eli5": "Test ELI5 summary",
            "key_metrics": {
                "total_financial_exposure": "Uncapped",
                "payment_terms": "Net-60",
                "termination_notice": "3 days",
                "governing_jurisdiction": "Delaware"
            },
            "red_flags": [
                {
                    "id": "RF-1",
                    "clause_reference": "Section 6",
                    "category": "Liability",
                    "problem": "Uncapped liability",
                    "real_world_consequence": "Bankruptcy risk",
                    "recommended_remedy": "Cap liability"
                }
            ],
            "action_checklist": ["Checklist item 1"]
        }
        report = legal_access_engine.generate_legal_audit_report(
            "Test Agreement", "Party A & Party B", mock_analysis
        )
        self.assertIn("# LEGALLENS AI — COMPREHENSIVE LEGAL AUDIT REPORT", report)
        self.assertIn("48 / 100", report)
        self.assertIn("RF-1", report)

    def test_api_route_translate(self):
        """Verify /api/legal-access/translate endpoint."""
        res = self.app.post("/api/legal-access/translate",
                            data=json.dumps({"text": "Test clause", "target_language": "Hindi"}),
                            content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["target_language"], "Hindi")


if __name__ == "__main__":
    unittest.main()
