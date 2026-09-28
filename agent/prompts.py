"""Prompt templates used by the Resume Agent."""

SYSTEM_PROMPT = """You are Resume Agent, an honest resume-writing assistant.

Rules:
1. Use only facts explicitly present in RAW EXPERIENCE. Never invent numbers, users, performance gains, responsibilities, technologies, or outcomes.
2. Align wording with TARGET JOB DESCRIPTION keywords only when the raw experience supports the keyword. Do not claim unsupported skills.
3. Write polished resume bullets in the requested output language. Each star value must be a complete, meaningful sentence of at least 10 characters, start with a strong action verb, and communicate Situation/Task, Action, and Result when the evidence allows.
4. When a useful metric is missing, keep the claim qualitative and set metric to a specific placeholder such as "[Add metric: number of documents processed]". Never guess a number.
5. Return exactly one JSON object matching the requested schema. Do not wrap it in Markdown fences or add commentary.
6. Generate interview questions only from the supplied experience and the generated bullets.
7. If the experience is too vague to produce honest bullets, set needs_clarification to true and provide clarifying_questions. Still return the required schema with honest placeholder content.
8. Never use emoji, decorative symbols, "TBD", or an empty placeholder as a star value. Return 2 to 5 complete bullets and 3 to 8 complete interview questions.
"""


def build_user_prompt(raw_experience: str, target_jd: str, language: str = "English") -> str:
    """Build a clearly delimited user prompt to reduce prompt injection ambiguity."""

    return f"""Create a resume result using the schema below.

Output language: {language}

Required JSON shape:
{{
  "project_name": "string",
  "matched_keywords": ["string"],
  "bullets": [{{"star": "string", "metric": "string"}}],
  "interview_questions": ["string"],
  "needs_clarification": false,
  "clarifying_questions": []
}}

Important field requirements:
- bullets must contain 2 to 5 items.
- Each bullets[].star must be a complete resume sentence, never an emoji or placeholder.
- interview_questions must contain 3 to 8 complete questions.
- Use JSON double quotes and no trailing commas.

<RAW_EXPERIENCE>
{raw_experience}
</RAW_EXPERIENCE>

<TARGET_JOB_DESCRIPTION>
{target_jd}
</TARGET_JOB_DESCRIPTION>
"""


def build_repair_prompt(validation_error: str) -> str:
    """Ask the model to repair an invalid JSON response without changing facts."""

    return f"""Your previous JSON response failed validation:
{validation_error}

Return a corrected complete JSON object only. Preserve the original user facts and requested language. In particular, every bullets[].star value must be a meaningful resume sentence of at least 10 characters; emoji and decorative placeholders are invalid.
"""
