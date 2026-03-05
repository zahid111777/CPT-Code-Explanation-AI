import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Load API key from keys/.env ──────────────────────────────────────────────
env_path = Path(__file__).resolve().parents[2] / "keys" / ".env"
load_dotenv(dotenv_path=env_path)

# ── LLM ─────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
)

# ── Prompt template ──────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a medical coding expert specializing in CPT \
(Current Procedural Terminology) codes.

When given a CPT code, respond with a clearly structured explanation that includes:

1. **Procedure Name** – The official name of the procedure.
2. **Description** – A detailed but easy-to-understand description of what \
the procedure involves.
3. **Medical Specialty** – The specialty typically associated with this code.
4. **Common Use Cases** – When and why this procedure is typically performed.
5. **Key Notes** – Important billing, coding, or clinical notes \
(e.g., bundling rules, documentation requirements).

If the CPT code is invalid or unrecognised, clearly state that and advise the \
user to verify it via the AMA CPT database.

Respond in a professional, informative manner suitable for both medical \
professionals and administrative staff."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Please explain CPT code: {cpt_code}"),
    ]
)

# ── Chain ────────────────────────────────────────────────────────────────────
chain = prompt | llm | StrOutputParser()


# ── Public helpers ───────────────────────────────────────────────────────────
def get_cpt_explanation(cpt_code: str) -> str:
    """Return a full explanation string for the given CPT code."""
    return chain.invoke({"cpt_code": cpt_code.strip()})


def stream_cpt_explanation(cpt_code: str):
    """Yield explanation tokens one at a time (for streaming UIs)."""
    for chunk in chain.stream({"cpt_code": cpt_code.strip()}):
        yield chunk
