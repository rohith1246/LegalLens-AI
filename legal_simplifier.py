"""
Legal Document Simplifier Module — LegalLens AI.
Directly implements Pillar 1 of the PromptWars 2026 Problem Statement:
"AI for Legal Assistance & Access: Engineer GenAI solutions to simplify complex legal docs..."

Key Capabilities:
- Plain-English (Layman/ELI5) translation of dense contracts
- Executive Commercial Briefing & key financial metrics extraction
- Automated 0–100 Legal Health Score & Risk Radar
- 3-Column Rights vs. Obligations Matrix
- Categorized Red-Flag Vulnerability Scanning with actionable countermeasures
"""

import logging
from typing import Dict, Any, Optional
import groq_service

logger = logging.getLogger("LegalDocSimplifier")


class LegalDocSimplifier:
    """
    Enterprise-grade engine for simplifying complex legal documents.
    Transforms dense legal jargon into accessible, actionable insights.
    """

    def __init__(self, default_api_key: Optional[str] = None):
        self.default_api_key = default_api_key

    def simplify_document(self, contract_text: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes complete simplification and risk assessment of a legal agreement.

        Args:
            contract_text: Full text of the contract or legal agreement.
            user_api_key: Optional client-provided Groq API key.

        Returns:
            Dictionary containing overall_health_score, risk_tier, executive_summary,
            layman_eli5, key_metrics, red_flags, rights_and_obligations, and action_checklist.
        """
        api_key = user_api_key or self.default_api_key
        logger.info(f"Simplifying legal document ({len(contract_text):,} characters)...")
        return groq_service.analyze_contract(contract_text, user_api_key=api_key)

    def extract_rights_and_obligations(self, contract_text: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
        """Extracts the 3-way matrix of your rights, your obligations, and counterparty obligations."""
        analysis = self.simplify_document(contract_text, user_api_key)
        return analysis.get("rights_and_obligations", {
            "your_rights": [],
            "your_obligations": [],
            "counterparty_obligations": []
        })

    def audit_risk_radar(self, contract_text: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
        """Returns categorized legal red flags, severity ratings, and actionable remedies."""
        analysis = self.simplify_document(contract_text, user_api_key)
        return {
            "health_score": analysis.get("overall_health_score", 50),
            "risk_tier": analysis.get("risk_tier", "Moderate Risk"),
            "red_flags": analysis.get("red_flags", []),
            "action_checklist": analysis.get("action_checklist", [])
        }


# Global default instance
simplifier_engine = LegalDocSimplifier()


def simplify_legal_document(contract_text: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
    """Functional convenience wrapper for document simplification."""
    return simplifier_engine.simplify_document(contract_text, user_api_key)
