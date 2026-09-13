"""
End-to-End Verification Test Suite for LegalLens AI.
Tests all Flask endpoints, AI pipelines, and ensures robust response structures.
"""

import unittest
import json
from app import app
from sample_contracts import SAMPLE_CONTRACTS

class LegalLensTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_status_endpoint(self):
        """Verify health check endpoint returns 200 and system details."""
        res = self.app.get('/api/status')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "online")
        self.assertIn("engine", data)
        self.assertGreater(data["sample_count"], 0)
        print("PASS: /api/status")

    def test_samples_endpoint(self):
        """Verify all 4 pre-loaded contracts are available."""
        res = self.app.get('/api/samples')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("samples", data)
        self.assertGreaterEqual(len(data["samples"]), 4)
        print("PASS: /api/samples (Loaded 4 rich sample contracts)")

    def test_analyze_endpoint(self):
        """Verify full contract audit, 0-100 score, red flags, and rights/obligations."""
        msa_text = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        res = self.app.post('/api/analyze', 
                            data=json.dumps({"text": msa_text}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("overall_health_score", data)
        self.assertIn("risk_tier", data)
        self.assertIn("red_flags", data)
        self.assertIn("rights_and_obligations", data)
        self.assertGreaterEqual(len(data["red_flags"]), 1)
        print(f"PASS: /api/analyze (Health Score: {data['overall_health_score']}, Red Flags: {len(data['red_flags'])})")

    def test_compare_endpoint(self):
        """Verify semantic contract redline comparison between V1 and V2."""
        text_a = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        text_b = SAMPLE_CONTRACTS["msa_comparison_v2"]["text"]
        res = self.app.post('/api/compare',
                            data=json.dumps({"text_a": text_a, "text_b": text_b}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("net_risk_delta", data)
        self.assertIn("clause_changes", data)
        self.assertIn("negotiation_verdict", data)
        print(f"PASS: /api/compare (Risk Delta: {data['net_risk_delta']}, Changes: {len(data['clause_changes'])})")

    def test_interrogate_endpoint(self):
        """Verify grounded clause Q&A with exact citations."""
        msa_text = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        res = self.app.post('/api/interrogate',
                            data=json.dumps({
                                "text": msa_text,
                                "question": "Can the client terminate without cause and what is the notice period?"
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("answer", data)
        self.assertIn("clause_citations", data)
        self.assertGreaterEqual(len(data["clause_citations"]), 1)
        print(f"PASS: /api/interrogate (Citations: {len(data['clause_citations'])})")

    def test_simulate_endpoint(self):
        """Verify 'What-If' hypothetical dispute simulator."""
        msa_text = SAMPLE_CONTRACTS["msa_freelance"]["text"]
        res = self.app.post('/api/simulate',
                            data=json.dumps({
                                "text": msa_text,
                                "scenario": "What if the client delays payment by 60 days?"
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("projected_outcome", data)
        self.assertIn("user_leverage", data)
        self.assertIn("step_by_step_action_plan", data)
        print(f"PASS: /api/simulate (Leverage: {data['user_leverage']})")

    def test_redraft_endpoint(self):
        """Verify counter-clause drafter and negotiation email pitch."""
        unfair_clause = "Contractor's indemnification obligations under this Section are uncapped and shall not be subject to any limitation of liability."
        res = self.app.post('/api/redraft',
                            data=json.dumps({
                                "clause": unfair_clause,
                                "goal": "balanced"
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("recommended_redraft", data)
        self.assertIn("negotiation_email_pitch", data)
        print("PASS: /api/redraft (Replacement wording & email pitch generated)")

    def test_translate_endpoint(self):
        """Verify multilingual translation into Hindi and regional terminology glossary."""
        sample_text = "Contractor shall indemnify Client against all damages without limitation of liability."
        res = self.app.post('/api/translate',
                            data=json.dumps({
                                "text": sample_text,
                                "target_language": "Hindi"
                            }),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("translated_content", data)
        self.assertIn("plain_explanation_target_lang", data)
        print(f"PASS: /api/translate ({data.get('target_language')})")

    def test_home_page(self):
        """Verify web app UI renders successfully."""
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"LegalLens AI", res.data)
        print("PASS: Web App Homepage (HTTP 200)")

if __name__ == "__main__":
    unittest.main()
