"""
Clause Clarifier & Interrogator Module — LegalLens AI.
Directly implements Pillar 3 of the PromptWars 2026 Problem Statement:
"AI for Legal Assistance & Access: ...or clarify clauses."

Key Capabilities:
- Grounded Clause Interrogation with verbatim citations and quote snippets
- "What-If" Real-World Dispute Simulator (leverage calculation, actionable steps, pitfalls)
- Smart Counter-Clause Drafter (Mutual/Balanced, User-Protective, Plain English)
- Ready-to-send counterparty negotiation email pitch generation
"""

import logging
from typing import Dict, Any, List, Optional
import groq_service

logger = logging.getLogger("ClauseClarifier")


class ClauseClarifier:
    """
    Enterprise-grade engine for interrogating, stress-testing, and clarifying legal clauses.
    Ensures complete transparency and negotiation leverage for contract signatories.
    """

    def __init__(self, default_api_key: Optional[str] = None):
        self.default_api_key = default_api_key

    def clarify_clause(
        self, 
        contract_text: str, 
        question: str, 
        chat_history: Optional[List[Dict[str, str]]] = None, 
        user_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Interrogates contract text to answer specific legal questions with exact citations.

        Args:
            contract_text: Full agreement text.
            question: Specific user query (e.g., termination terms, liability caps).
            chat_history: Optional recent conversation context.
            user_api_key: Optional client-provided Groq API key.

        Returns:
            Dictionary containing answer, clause_citations list, tactical_advice, and suggested_followups.
        """
        api_key = user_api_key or self.default_api_key
        logger.info(f"Clarifying clause for question: '{question[:80]}...'")
        return groq_service.interrogate_clause(
            contract_text, 
            question, 
            chat_history=chat_history or [], 
            user_api_key=api_key
        )

    def simulate_what_if_scenario(
        self, 
        contract_text: str, 
        scenario: str, 
        user_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Simulates a real-world legal dilemma against contract terms before signing.

        Args:
            contract_text: Active contract text.
            scenario: Hypothetical situation (e.g. 60-day payment delay, early termination).
            user_api_key: Optional client-provided Groq API key.

        Returns:
            Dictionary containing scenario_title, projected_outcome, user_leverage,
            applicable_clauses, financial_or_legal_exposure, step_by_step_action_plan, and traps_to_avoid.
        """
        api_key = user_api_key or self.default_api_key
        logger.info(f"Simulating what-if scenario: '{scenario[:80]}...'")
        return groq_service.simulate_scenario(contract_text, scenario, user_api_key=api_key)

    def redraft_clause(
        self, 
        clause_text: str, 
        goal: str = "balanced", 
        context: str = "", 
        user_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Rewrites an unfair or one-sided clause into an enforceable, balanced replacement.

        Args:
            clause_text: Target unfair clause text.
            goal: Redraft strategy ('balanced', 'protective', or 'plain_english').
            context: Optional surrounding agreement text.
            user_api_key: Optional client-provided Groq API key.

        Returns:
            Dictionary containing original_clause_critique, recommended_redraft,
            key_improvements list, and negotiation_email_pitch.
        """
        api_key = user_api_key or self.default_api_key
        logger.info(f"Redrafting clause with strategy: '{goal}'...")
        return groq_service.redraft_clause(
            clause_text, 
            redraft_goal=goal, 
            contract_context=context, 
            user_api_key=api_key
        )


# Global default instance
clarifier_engine = ClauseClarifier()


def clarify_legal_clause(
    contract_text: str, 
    question: str, 
    chat_history: Optional[List[Dict[str, str]]] = None, 
    user_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Functional convenience wrapper for clause clarification."""
    return clarifier_engine.clarify_clause(contract_text, question, chat_history, user_api_key)
