"""Streamlit UI for Resume Agent MVP."""

import json
from pathlib import Path

import streamlit as st

from agent.core import ResumeAgentError, generate_resume
from agent.schemas import ResumeResult

st.set_page_config(page_title="Resume Agent", page_icon="📄", layout="wide")

EXAMPLES_DIR = Path(__file__).parent / "examples"


def load_example(filename: str) -> str:
    return (EXAMPLES_DIR / filename).read_text(encoding="utf-8")


def result_to_markdown(result: ResumeResult) -> str:
    lines = [f"# {result.project_name}", "", "## Matched keywords", ", ".join(result.matched_keywords) or "None", "", "## Resume bullets"]
    for bullet in result.bullets:
        lines.extend([f"- {bullet.star}", f"  - Metric to verify: {bullet.metric}"])
    lines.extend(["", "## Interview questions"])
    lines.extend(f"- {question}" for question in result.interview_questions)
    if result.needs_clarification:
        lines.extend(["", "## Clarifying questions"])
        lines.extend(f"- {question}" for question in result.clarifying_questions)
    return "\n".join(lines)


st.title("Resume Agent")
st.caption("把原始经历转成诚实、匹配 JD 的英文简历 bullet，并生成面试准备问题。")

if "raw_experience" not in st.session_state:
    st.session_state.raw_experience = ""
if "target_jd" not in st.session_state:
    st.session_state.target_jd = ""

with st.sidebar:
    st.header("输入设置")
    language = st.selectbox("输出语言", ["English", "中文"], index=0)
    if st.button("载入示例", use_container_width=True):
        st.session_state.raw_experience = load_example("input_experience.txt")
        st.session_state.target_jd = load_example("target_jd.txt")
        st.rerun()
    st.divider()
    st.markdown("**诚实性规则**")
    st.caption("模型不会猜测数字。缺少数据时会显示 [Add metric: ...]，请在提交简历前核实并补充。")

left, right = st.columns(2)
with left:
    raw_experience = st.text_area(
        "原始经历",
        key="raw_experience",
        height=280,
        placeholder="例如：我用 LangChain 和 Chroma 构建了一个可以查询 PDF 的 RAG 聊天机器人。",
    )
with right:
    target_jd = st.text_area(
        "目标职位描述（JD）",
        key="target_jd",
        height=280,
        placeholder="粘贴目标职位的职责和要求。",
    )

if st.button("生成简历 Bullet", type="primary", use_container_width=True):
    if not raw_experience.strip() or not target_jd.strip():
        st.error("请同时填写原始经历和目标职位描述。")
    else:
        with st.spinner("正在生成并校验结构化结果…"):
            try:
                st.session_state.result = generate_resume(raw_experience, target_jd, language)
            except ResumeAgentError as exc:
                st.error(str(exc))
            except Exception as exc:  # Keep unexpected UI failures readable.
                st.error(f"发生未预期错误：{exc}")

result = st.session_state.get("result")
if result:
    st.divider()
    st.subheader(result.project_name)
    if result.matched_keywords:
        st.markdown("**匹配关键词：** " + " · ".join(f"`{keyword}`" for keyword in result.matched_keywords))

    st.markdown("### Resume bullets")
    for index, bullet in enumerate(result.bullets, start=1):
        st.markdown(f"**{index}.** {bullet.star}")
        st.info(f"Metric to verify: {bullet.metric}")

    if result.needs_clarification:
        st.warning("信息还不够完整，请补充以下内容：")
        for question in result.clarifying_questions:
            st.markdown(f"- {question}")

    st.markdown("### Interview questions")
    for question in result.interview_questions:
        st.markdown(f"- {question}")

    markdown_output = result_to_markdown(result)
    st.download_button("下载 Markdown", markdown_output, file_name="resume-agent-result.md", mime="text/markdown")
    with st.expander("查看原始 JSON"):
        st.code(json.dumps(result.model_dump(), ensure_ascii=False, indent=2), language="json")
