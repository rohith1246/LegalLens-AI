"""
Contract Comparator & Redliner Module — LegalLens AI.
Directly implements Pillar 2 of the PromptWars 2026 Problem Statement:
"AI for Legal Assistance & Access: ...compare contracts..."

Key Capabilities:
- Semantic Contract Redlining (intent changes vs mere word formatting)
- Favorable vs Unfavorable shift classification
- Net Risk Delta calculation (+/- Safety Points)
- Missing protections detection
- Conclusive executive negotiation verdict
"""

import logging
from typing import Dict, Any, Optional
import groq_service

logger = logging.getLogger("ContractComparator")


class ContractComparator:
    """
    Enterprise-grade contract comparison and semantic redlining engine.
    Performs substantive legal intent diffing across agreement revisions.
    """

    def __init__(self, default_api_key: Optional[str] = None):
        self.default_api_key = default_api_key

    def compare_contracts(self, text_a: str, text_b: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Compares Version 1 (Baseline) against Version 2 (Redline/Markup).

        Args:
            text_a: Version 1 baseline contract text.
            text_b: Version 2 revised contract text.
            user_api_key: Optional client-provided Groq API key.

        Returns:
            Dictionary containing comparison_summary, net_risk_delta, score_delta,
            clause_changes list, missing_protections, and negotiation_verdict.
        """
        api_key = user_api_key or self.default_api_key
        logger.info(f"Comparing contracts: V1 ({len(text_a):,} chars) vs V2 ({len(text_b):,} chars)...")
        return groq_service.compare_contracts(text_a, text_b, user_api_key=api_key)

    def detect_semantic_shifts(self, text_a: str, text_b: str, user_api_key: Optional[str] = None) -> list:
        """Returns the list of substantive clause alterations with favorable/unfavorable ratings."""
        result = self.compare_contracts(text_a, text_b, user_api_key)
        return result.get("clause_changes", [])

    def calculate_risk_delta(self, text_a: str, text_b: str, user_api_key: Optional[str] = None) -> Dict[str, str]:
        """Returns the overall risk direction and numeric safety score shift."""
        result = self.compare_contracts(text_a, text_b, user_api_key)
        return {
            "net_risk_delta": result.get("net_risk_delta", "Neutral"),
            "score_delta": result.get("score_delta", "0 Points"),
            "verdict": result.get("negotiation_verdict", "Review changes manually")
        }


# Global default instance
comparator_engine = ContractComparator()


def compare_legal_contracts(text_a: str, text_b: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
    """Functional convenience wrapper for contract comparison."""
    return comparator_engine.compare_contracts(text_a, text_b, user_api_key)
