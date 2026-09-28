"""LLM integration and validation for Resume Agent."""

import json
import os
from typing import Any, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from .prompts import SYSTEM_PROMPT, build_repair_prompt, build_user_prompt
from .schemas import ResumeResult

load_dotenv()


class ResumeAgentError(RuntimeError):
    """User-facing error for configuration, provider, or validation failures."""


def _get_client() -> tuple[OpenAI, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base_url = os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/").strip()
    model_name = os.getenv("MODEL_NAME", "glm-4-flash").strip()
    if not api_key or api_key == "your_zhipu_api_key_here":
        raise ResumeAgentError("未配置 OPENAI_API_KEY。请复制 .env.example 为 .env，并填入智谱 API Key。")
    if not model_name:
        raise ResumeAgentError("MODEL_NAME 不能为空，请检查 .env 配置。")
    return OpenAI(api_key=api_key, base_url=base_url), model_name


def _extract_content(response: Any) -> str:
    try:
        content: Optional[str] = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError) as exc:
        raise ResumeAgentError("模型返回了无法识别的响应。") from exc
    if not content or not content.strip():
        raise ResumeAgentError("模型没有返回内容，请稍后重试。")
    return content.strip()


def _validate_content(content: str) -> ResumeResult:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("返回内容不是合法 JSON") from exc
    try:
        return ResumeResult.model_validate(payload)
    except ValidationError as exc:
        errors = []
        for error in exc.errors(include_url=False, include_input=False):
            location = ".".join(str(part) for part in error["loc"])
            errors.append(f"{location}: {error['msg']}")
        raise ValueError("；".join(errors)) from exc


def generate_resume(raw_experience: str, target_jd: str, language: str = "English") -> ResumeResult:
    """Generate and validate structured resume content using an OpenAI-compatible API."""

    if not raw_experience.strip():
        raise ResumeAgentError("请先填写原始经历。")
    if not target_jd.strip():
        raise ResumeAgentError("请先填写目标职位描述。")

    client, model_name = _get_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(raw_experience, target_jd, language)},
    ]

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=model_name,
                temperature=0.2 if attempt == 0 else 0,
                response_format={"type": "json_object"},
                messages=messages,
            )
        except Exception as exc:
            raise ResumeAgentError(f"调用模型失败：{exc}") from exc

        content = _extract_content(response)
        try:
            return _validate_content(content)
        except ValueError as exc:
            if attempt == 1:
                raise ResumeAgentError("模型连续两次返回了不完整内容，请再次点击生成或更换模型后重试。") from exc
            messages.extend(
                [
                    {"role": "assistant", "content": content},
                    {"role": "user", "content": build_repair_prompt(str(exc))},
                ]
            )

    raise ResumeAgentError("模型未能生成有效内容，请重试。")
