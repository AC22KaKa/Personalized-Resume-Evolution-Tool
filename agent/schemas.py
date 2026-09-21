"""Pydantic models for validated resume generation results."""

from typing import List

from pydantic import BaseModel, Field, field_validator, model_validator


class ResumeBullet(BaseModel):
    """One concise, STAR-oriented resume bullet."""

    star: str = Field(min_length=10, description="A polished resume bullet using STAR evidence.")
    metric: str = Field(min_length=1, description="A verified metric or an Add metric placeholder.")


class ResumeResult(BaseModel):
    """The complete structured response returned by the resume agent."""

    project_name: str = Field(min_length=1)
    matched_keywords: List[str] = Field(default_factory=list)
    bullets: List[ResumeBullet] = Field(min_length=2, max_length=5)
    interview_questions: List[str] = Field(min_length=3, max_length=8)
    needs_clarification: bool = False
    clarifying_questions: List[str] = Field(default_factory=list)

    @field_validator("matched_keywords", "interview_questions", "clarifying_questions")
    @classmethod
    def strip_text_items(cls, value: List[str]) -> List[str]:
        cleaned = [item.strip() for item in value]
        if any(not item for item in cleaned):
            raise ValueError("Text lists cannot contain empty items")
        return cleaned

    @model_validator(mode="after")
    def validate_clarification_state(self) -> "ResumeResult":
        if self.needs_clarification and not self.clarifying_questions:
            raise ValueError("clarifying_questions is required when needs_clarification is true")
        if not self.needs_clarification and self.clarifying_questions:
            raise ValueError("clarifying_questions must be empty when clarification is not needed")
        return self
