import pytest
from pydantic import ValidationError

from agent.schemas import ResumeResult


def valid_payload() -> dict:
    return {
        "project_name": "LLM Knowledge Base Assistant",
        "matched_keywords": ["RAG", "Chroma"],
        "bullets": [
            {"star": "Built a RAG assistant using LangChain and Chroma to answer questions from PDF documents.", "metric": "[Add metric: number of documents processed]"},
            {"star": "Deployed the assistant on Streamlit Cloud and resolved dependency and secret-management issues.", "metric": "[Add metric: deployment time or uptime]"},
        ],
        "interview_questions": [
            "How did you choose the chunking strategy?",
            "How did you evaluate retrieval quality?",
            "How would you reduce hallucinations in production?",
        ],
        "needs_clarification": False,
        "clarifying_questions": [],
    }


def test_valid_payload_parses_and_preserves_metric_placeholder():
    result = ResumeResult.model_validate(valid_payload())
    assert len(result.bullets) == 2
    assert result.bullets[0].metric.startswith("[Add metric:")


def test_missing_required_field_fails_validation():
    payload = valid_payload()
    del payload["project_name"]
    with pytest.raises(ValidationError):
        ResumeResult.model_validate(payload)


def test_bullet_and_question_types_are_validated():
    payload = valid_payload()
    payload["bullets"][0]["star"] = 123
    with pytest.raises(ValidationError):
        ResumeResult.model_validate(payload)


def test_clarification_requires_questions():
    payload = valid_payload()
    payload["needs_clarification"] = True
    with pytest.raises(ValidationError):
        ResumeResult.model_validate(payload)

