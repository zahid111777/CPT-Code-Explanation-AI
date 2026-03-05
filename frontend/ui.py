import sys
from pathlib import Path

# Make the project root importable so `backend.src.main` resolves correctly
# regardless of where `chainlit run` is invoked from.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import chainlit as cl
from backend.src.main import stream_cpt_explanation

# ── Welcome banner ───────────────────────────────────────────────────────────
WELCOME = """## CPT Code Explanation AI

I can explain any **CPT (Current Procedural Terminology) code** instantly.

Just type a CPT code — for example `99213`, `27447`, or `70553` — and I will return:

- **Procedure name & description**
- **Medical specialty**
- **Common use cases**
- **Billing & coding notes**

---
*Enter a CPT code below to get started.*"""


# ── Chainlit hooks ───────────────────────────────────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content=WELCOME).send()


@cl.on_message
async def on_message(message: cl.Message):
    cpt_code = message.content.strip()

    if not cpt_code:
        await cl.Message(content="Please enter a CPT code to continue.").send()
        return

    # Start an empty streaming message
    response_msg = cl.Message(content="")
    await response_msg.send()

    try:
        for token in stream_cpt_explanation(cpt_code):
            await response_msg.stream_token(token)
    except Exception as exc:
        response_msg.content = f"**Error:** {exc}"
        await response_msg.update()
