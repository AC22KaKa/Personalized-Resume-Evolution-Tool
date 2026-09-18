# Resume Agent — AI-Powered Resume Bullet Generator

An AI tool that turns rough project notes and work experience into polished, JD-tailored resume bullets using the STAR method.

> Built for students, career switchers, and developers who know what they did — but not how to write it for recruiters and hiring managers.

---

## Overview

**Resume Agent** helps you transform messy experience descriptions into professional resume content.

You provide:

- Your raw experience, project notes, or GitHub README
- A target job description (JD)

The tool returns:

- JD-matched resume bullets
- STAR-structured descriptions
- Quantification suggestions
- Missing metric placeholders
- Likely interview questions based on the generated resume

This project is designed as a practical LLM application and portfolio project. It combines prompt engineering, structured output, optional RAG, and a simple Streamlit interface.

---

## Why This Project?

Most people do not struggle because they lack experience. They struggle because they do not know how to present it.

ChatGPT can help, but generic chat often produces:

- Vague bullets
- Fabricated metrics
- Poor JD alignment
- Inconsistent formatting
- No interview preparation

**Resume Agent** solves this by enforcing structure, JD alignment, and anti-hallucination rules.

It is not just a chatbot. It is a focused AI writing assistant for career documents.

---

## Features

- **JD-aware bullet generation** — aligns your experience with the target role
- **STAR method formatting** — Situation, Task, Action, Result
- **Quantification prompts** — suggests where to add metrics
- **Anti-hallucination guardrails** — never invents numbers; uses placeholders instead
- **Structured JSON output** — powered by Pydantic schemas
- **Interview question generator** — predicts questions from your generated resume
- **Streamlit UI** — simple, fast, and easy to deploy
- **OpenAI-compatible API support** — works with OpenAI, DashScope/Qwen, Ollama, and more
- **Optional RAG mode** — retrieve details from your project READMEs and docs

---

## Demo

> Add a screenshot or short GIF here.

Example workflow:

1. Paste your rough experience
2. Paste the target JD
3. Click **Generate Resume Bullets**
4. Copy the results into your resume
5. Click **Generate Interview Questions** to prepare

---

## How It Works

```text
User Input
   |
   v
Raw Experience + Target JD
   |
   v
LLM Prompt + Pydantic Schema
   |
   v
Structured Resume Bullets
   |
   v
Interview Question Generator
   |
   v
Markdown / JSON Output
```

Optional RAG mode:

```text
GitHub README / Project Docs
   |
   v
Text Splitter -> Embeddings -> Chroma
   |
   v
Relevant Project Context
   |
   v
LLM Prompt
```

---

## Tech Stack

- **Python 3.10+**
- **Streamlit** — UI
- **LangChain / OpenAI SDK** — LLM orchestration
- **Pydantic** — structured output validation
- **Chroma** — optional vector database for RAG
- **OpenAI-compatible APIs** — OpenAI, DashScope/Qwen, Ollama, etc.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- An API key for an OpenAI-compatible model provider
- Git

### Installation

```bash
git clone https://github.com/your-username/resume-agent.git
cd resume-agent

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Example `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
```

For DashScope / Qwen:

```env
OPENAI_API_KEY=your_dashscope_key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-max
```

For local Ollama:

```env
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
MODEL_NAME=qwen2.5:7b
```

### Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal.

---

## Usage

### Input

**Raw Experience**

```text
I built a RAG chatbot using LangChain and Chroma. It answers questions from PDFs.
I deployed it on Streamlit Cloud. I fixed deployment issues with requirements.txt and secrets.
```

**Target JD**

```text
We are looking for an LLM Application Engineer with experience in RAG,
vector databases, evaluation, and deployment.
```

### Output

```json
{
  "project_name": "LLM Knowledge Base Assistant",
  "matched_keywords": ["RAG", "LangChain", "Chroma", "Streamlit"],
  "bullets": [
    {
      "star": "Built a RAG-based knowledge assistant using LangChain and Chroma, enabling users to query PDF documents in natural language.",
      "metric": "[Add: number of documents / users / latency improvement]"
    },
    {
      "star": "Deployed the application on Streamlit Cloud and resolved dependency and secret-management issues for a stable public demo.",
      "metric": "[Add: uptime / deployment time / user feedback]"
    }
  ],
  "interview_questions": [
    "How did you evaluate the retrieval quality of your RAG system?",
    "What chunking strategy did you use, and why?",
    "How would you reduce hallucination in a production RAG pipeline?"
  ]
}
```

---

## Project Structure

```text
resume-agent/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── agent/
│   ├── __init__.py
│   ├── core.py
│   ├── prompts.py
│   └── schemas.py
├── tools/
│   ├── __init__.py
│   └── resume_tools.py
├── data/
│   └── examples/
├── tests/
│   └── test_schemas.py
└── examples/
    ├── input_experience.txt
    └── target_jd.txt
```

---

## Guardrails

Resume Agent follows strict rules to keep your resume honest and useful.

- **No fabricated metrics** — if no data exists, the model outputs `[Add metric]`
- **JD alignment only** — it does not invent skills you did not mention
- **Structured output** — every response must match the Pydantic schema
- **Explicit uncertainty** — if the input is too vague, the tool asks for clarification
- **User confirmation** — generated content should always be reviewed before use

---

## Roadmap

- [ ] PDF / DOCX export
- [ ] LaTeX resume template
- [ ] LinkedIn summary generator
- [ ] Cover letter generator
- [ ] Multi-language support
- [ ] RAG over GitHub repositories
- [ ] Evaluation dashboard with fixed test cases
- [ ] Local-first mode with Ollama
- [ ] Browser extension for job applications

---

## Evaluation

This project can be evaluated with a small fixed test set.

Metrics to track:

- JD keyword match rate
- STAR compliance
- Fabricated metric rate
- User edit distance
- Interview question relevance
- Latency and cost per generation

A simple `evals/` folder can contain:

```text
evals/
├── cases.json
└── evaluate.py
```

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

Please keep the project focused, practical, and honest.

---

## License

MIT License.

---

## Acknowledgements

- Inspired by the need for better career tools for students and career switchers
- Built as part of an LLM application development learning journey
- Thanks to the open-source LLM community

---

## Disclaimer

This tool is designed to help you write better resumes, not to fabricate experience.

Always review, edit, and verify every generated bullet before submitting it to a recruiter or company.
