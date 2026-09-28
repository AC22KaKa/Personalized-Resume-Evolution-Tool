import json

from agent import core


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeChoice:
    def __init__(self, content: str):
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, payload: dict):
        self.choices = [FakeChoice(json.dumps(payload))]


class FakeCompletions:
    def __init__(self, payloads: list[dict]):
        self.payloads = payloads
        self.last_kwargs = None
        self.calls = []

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        self.calls.append(kwargs)
        return FakeResponse(self.payloads.pop(0))


class FakeClient:
    def __init__(self, payloads: list[dict]):
        self.chat = type("Chat", (), {"completions": FakeCompletions(payloads)})()


def payload() -> dict:
    return {
        "project_name": "Demo Assistant",
        "matched_keywords": ["RAG"],
        "bullets": [
            {"star": "Built a retrieval assistant from project documents.", "metric": "[Add metric: document count]"},
            {"star": "Deployed the assistant and resolved configuration issues.", "metric": "[Add metric: deployment time]"},
        ],
        "interview_questions": ["How did retrieval work?", "How did you test it?", "How would you improve it?"],
        "needs_clarification": False,
        "clarifying_questions": [],
    }


def test_generate_resume_validates_mocked_provider(monkeypatch):
    fake_client = FakeClient([payload()])
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("MODEL_NAME", "test-model")
    monkeypatch.setattr(core, "OpenAI", lambda **_: fake_client)

    result = core.generate_resume("Built a retrieval assistant.", "Looking for RAG experience.")

    assert result.project_name == "Demo Assistant"
    assert fake_client.chat.completions.last_kwargs["temperature"] == 0.2
    assert fake_client.chat.completions.last_kwargs["response_format"] == {"type": "json_object"}


def test_generate_resume_repairs_invalid_first_response(monkeypatch):
    invalid = payload()
    invalid["bullets"][0]["star"] = "✨"
    fake_client = FakeClient([invalid, payload()])
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(core, "OpenAI", lambda **_: fake_client)

    result = core.generate_resume("Built a retrieval assistant.", "Looking for RAG experience.")

    assert result.project_name == "Demo Assistant"
    assert len(fake_client.chat.completions.calls) == 2
    assert fake_client.chat.completions.calls[1]["temperature"] == 0
    assert "failed validation" in fake_client.chat.completions.calls[1]["messages"][-1]["content"]
