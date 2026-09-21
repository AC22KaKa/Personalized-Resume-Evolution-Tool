"""Core package for Resume Agent.

Keep package import lightweight so schema-only tooling does not initialize the
LLM client and its optional provider dependencies.
"""

from .schemas import ResumeBullet, ResumeResult

__all__ = ["ResumeBullet", "ResumeResult"]
