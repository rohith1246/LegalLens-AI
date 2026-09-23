"""
Tests for Pillar 3: Clarify Clauses.
Verifies grounded clause interrogation, what-if scenario simulations, and counter-clause drafting.
"""

import unittest
import json
from app import app
from sample_contracts import SAMPLE_CONTRACTS
from clause_clarifier import clarifier_engine


class ClarifyClausesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.text = SAMPLE_CONTRACTS["msa_freelance"]["text"]

    def test_clarify_clause_grounded_citations(self):
        """Verify clause interrogation returns exact quotes and citations."""
        res = clarifier_engine.clarify_clause(
            self.text,
            "Can the client terminate without cause and what notice is required?"
        )
        self.assertIn("answer", res)
        self.assertIn("clause_citations", res)
        self.assertGreaterEqual(len(res["clause_citations"]), 1)
        self.assertTrue(res["clause_citations"][0]["quote"])

    def test_simulate_what_if_scenario(self):
        """Verify what-if scenario simulation output and user leverage."""
        res = clarifier_engine.simulate_what_if_scenario(
            self.text,
            "What if client delays payment by 60 days?"
        )
        self.assertIn("projected_outcome", res)
        self.assertIn("user_leverage", res)
        self.assertIn("step_by_step_action_plan", res)
        self.assertIn("traps_to_avoid", res)

    def test_redraft_clause_balanced(self):
        """Verify counter-clause drafter and negotiation email pitch."""
        unfair_clause = "Contractor's indemnification obligations are uncapped with no limitation of liability."
        res = clarifier_engine.redraft_clause(unfair_clause, goal="balanced")
        
        self.assertIn("recommended_redraft", res)
        self.assertIn("negotiation_email_pitch", res)
        self.assertIn("Mutual", res["recommended_redraft"])

    def test_api_route_clarify_clauses(self):
        """Verify dedicated /api/clarify-clauses endpoint."""
        res = self.app.post("/api/clarify-clauses",
                            data=json.dumps({
                                "text": self.text,
                                "question": "Who owns intellectual property created on weekends?"
                            }),
                            content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("answer", data)
        self.assertIn("clause_citations", data)


if __name__ == "__main__":
    unittest.main()
