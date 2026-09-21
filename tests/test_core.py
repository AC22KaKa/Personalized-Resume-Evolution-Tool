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
    def __init__(self, payload: dict):
        self.payload = payload
        self.last_kwargs = None

    def create(self, **kwargs):
        self.last_kwargs = kwargs
        return FakeResponse(self.payload)


class FakeClient:
    def __init__(self, payload: dict):
        self.chat = type("Chat", (), {"completions": FakeCompletions(payload)})()


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
    fake_client = FakeClient(payload())
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.invalid/v1")
    monkeypatch.setenv("MODEL_NAME", "test-model")
    monkeypatch.setattr(core, "OpenAI", lambda **_: fake_client)

    result = core.generate_resume("Built a retrieval assistant.", "Looking for RAG experience.")

    assert result.project_name == "Demo Assistant"
    assert fake_client.chat.completions.last_kwargs["temperature"] == 0.2
    assert fake_client.chat.completions.last_kwargs["response_format"] == {"type": "json_object"}

