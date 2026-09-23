"""
Pydantic Schemas for LegalLens AI.
Provides strict type validation, serialization, and defensive data modeling
for all legal assistance and contract intelligence operations.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, field_validator


class ContractAnalysisRequest(BaseModel):
    """Schema for document simplification and analysis requests."""
    text: str = Field(..., min_length=1, max_length=100000, description="Raw contract text to analyze")
    api_key: Optional[str] = Field(None, description="Optional custom Groq API key")

    @field_validator("text")
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Contract text cannot be empty or only whitespace.")
        return v.strip()


class ContractComparisonRequest(BaseModel):
    """Schema for dual-contract redline comparison requests."""
    text_a: str = Field(..., min_length=1, max_length=100000, description="Version 1 baseline contract text")
    text_b: str = Field(..., min_length=1, max_length=100000, description="Version 2 redline contract text")
    api_key: Optional[str] = Field(None, description="Optional custom Groq API key")

    @field_validator("text_a", "text_b")
    def text_fields_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Comparison contracts cannot be empty.")
        return v.strip()


class ClauseInterrogationRequest(BaseModel):
    """Schema for grounded clause Q&A requests."""
    text: str = Field(..., min_length=1, max_length=100000, description="Contract text to interrogate")
    question: str = Field(..., min_length=1, max_length=2000, description="User legal query")
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Prior conversation context")
    api_key: Optional[str] = Field(None, description="Optional custom Groq API key")


class ScenarioSimulationRequest(BaseModel):
    """Schema for hypothetical 'What-If' dispute simulation."""
    text: str = Field(..., min_length=1, max_length=100000, description="Active contract text")
    scenario: str = Field(..., min_length=1, max_length=3000, description="Hypothetical dispute scenario")
    api_key: Optional[str] = Field(None, description="Optional custom Groq API key")


class ClauseRedraftRequest(BaseModel):
    """Schema for counter-clause drafting requests."""
    clause: str = Field(..., min_length=1, max_length=5000, description="Target clause to redraft")
    goal: str = Field("balanced", description="Redraft strategy: balanced, protective, or plain_english")
    context: Optional[str] = Field("", max_length=10000, description="Surrounding contract context")
    api_key: Optional[str] = Field(None, description="Optional custom Groq API key")


class MultilingualTranslationRequest(BaseModel):
    """Schema for democratized legal access translation requests."""
    text: str = Field(..., min_length=1, max_length=10000, description="Legal text to translate")
    target_language: str = Field("Hindi", description="Target regional language")
    api_key: Optional[str] = Field(None, description="Optional custom Groq API key")
