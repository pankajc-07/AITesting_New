"""
app.py — Main chat screen for Jira Test Case Generator.

ChatGPT-style interface: user types a Jira issue key, the app fetches
the ticket, merges it into a test case template, generates test cases
via Ollama (or Groq fallback), and renders the result in the chat.
"""

import re
import sys
from pathlib import Path

import streamlit as st

# Ensure src/ is on sys.path for sibling imports
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config_store import load_settings
from jira_client import fetch_issue
from llm_client import generate_test_cases

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
TEMPLATE_PATH = SRC_DIR.parent / "Templates" / "testcase_creator.md"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Jira Test Case Generator",
    page_icon="🧪",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS for better table rendering
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Make tables fill width and look clean */
    .stMarkdown table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    .stMarkdown th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: 600;
        padding: 10px 12px;
        text-align: left;
    }
    .stMarkdown td {
        padding: 8px 12px;
        border-bottom: 1px solid #e0e0e0;
        vertical-align: top;
    }
    .stMarkdown tr:hover td {
        background-color: #f5f3ff;
    }
    /* Ticket info card */
    .ticket-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border: 1px solid #d4d8f0;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .ticket-card h4 {
        margin-top: 0;
        color: #4a4a8a;
    }
    /* Priority badges */
    .priority-high { color: #e53e3e; font-weight: bold; }
    .priority-medium { color: #dd6b20; font-weight: bold; }
    .priority-low { color: #38a169; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Sidebar — status & quick info
# ---------------------------------------------------------------------------
settings = load_settings()

with st.sidebar:
    st.title("🧪 Jira TC Generator")

    provider = settings.get("LLM_PROVIDER", "ollama")
    if provider == "ollama":
        st.info(f"🦙 **Ollama** — `{settings.get('OLLAMA_MODEL', 'gemma3:1b')}`")
    else:
        st.info(f"☁️ **Groq** — cloud API")

    jira_url = settings.get("JIRA_BASE_URL", "")
    if jira_url:
        st.success(f"🔗 Jira: `{jira_url}`")
    else:
        st.warning("⚠️ Jira not configured")

    st.divider()
    st.caption("Go to **Settings** page to configure credentials.")
    st.caption("Type a Jira key like `QA-102` to generate test cases.")

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I can generate test cases from your Jira tickets. Just type a Jira issue key (e.g., `QA-102`) and I'll fetch the ticket and create test cases for you."}
        ]
        st.rerun()

# ---------------------------------------------------------------------------
# Initialize chat history
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I can generate test cases from your Jira tickets. Just type a Jira issue key (e.g., `QA-102`) and I'll fetch the ticket and create test cases for you."}
    ]

# ---------------------------------------------------------------------------
# Render chat history
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_llm_output(text: str) -> str:
    """Post-process LLM output for better markdown rendering."""
    # Remove leading/trailing whitespace
    text = text.strip()
    # Ensure table headers have proper spacing
    text = re.sub(r'\|(\S)', r'| \1', text)
    text = re.sub(r'(\S)\|', r'\1 |', text)
    # Color-code priorities in the table
    text = text.replace('| High |', '| <span class="priority-high">🔴 High</span> |')
    text = text.replace('| Medium |', '| <span class="priority-medium">🟠 Medium</span> |')
    text = text.replace('| Low |', '| <span class="priority-low">🟢 Low</span> |')
    return text


def _build_ticket_card(ticket: dict) -> str:
    """Build a nice HTML card showing the Jira ticket details."""
    summary = ticket.get("summary", "N/A")
    description = ticket.get("description", "No description")[:500]
    ac = ticket.get("acceptance_criteria", "Not specified")[:500]
    key = ticket.get("key", "???")

    return f"""
<div class="ticket-card">
<h4>📋 Jira Ticket: {key}</h4>
<strong>Summary:</strong> {summary}<br><br>
<strong>Description:</strong><br><em>{description}</em><br><br>
<strong>Acceptance Criteria:</strong><br><em>{ac}</em>
</div>
"""

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Type a Jira issue key to generate test cases..."):
    # --- Add user message ---
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Parse Jira issue key ---
    match = re.search(r"[A-Z][A-Z0-9_]+-\d+", prompt, re.IGNORECASE)
    if not match:
        response = (
            "❌ I couldn't find a Jira issue key in your message.\n\n"
            "Please include a key like `QA-102` or `PROJ-123` in your request.\n\n"
            "Example: *\"create test cases for QA-102\"*"
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        issue_key = match.group(0).upper()

        # --- Step 1: Fetch Jira ticket ---
        with st.chat_message("assistant"):
            with st.spinner(f"🔍 Fetching `{issue_key}` from Jira..."):
                ticket = fetch_issue(issue_key)

            if not ticket["ok"]:
                response = f"❌ **Error fetching `{issue_key}`:** {ticket['error']}"
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response)
            else:
                # --- Step 2: Load template ---
                if TEMPLATE_PATH.exists():
                    template = TEMPLATE_PATH.read_text(encoding="utf-8")
                else:
                    response = f"❌ **Template not found** at `{TEMPLATE_PATH}`. Make sure `Templates/testcase_creator.md` exists."
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.markdown(response)
                    st.stop()

                # --- Step 3: Merge ticket into template ---
                merged_prompt = template.replace("[FEATURE]", ticket["summary"])
                merged_prompt = merged_prompt.replace(
                    "[PASTE REQUIREMENTS HERE]",
                    f"**Summary:** {ticket['summary']}\n\n"
                    f"**Description:**\n{ticket['description']}\n\n"
                    f"**Acceptance Criteria:**\n{ticket['acceptance_criteria']}",
                )

                # --- Step 4: Generate test cases ---
                with st.spinner(f"🤖 Generating test cases via {provider.upper()}..."):
                    result = generate_test_cases(merged_prompt)

                if result["ok"]:
                    provider_used = result["provider"]
                    cleaned = _clean_llm_output(result["response"])

                    # Build the full response
                    ticket_card = _build_ticket_card(ticket)
                    response = (
                        f"### ✅ Test Cases Generated\n\n"
                        f"{ticket_card}\n\n"
                        f"---\n\n"
                        f"{cleaned}\n\n"
                        f"---\n\n"
                        f"*Generated via **{provider_used}** · {len(cleaned.split(chr(10)))} lines*"
                    )
                else:
                    response = f"❌ **LLM Error:** {result['error']}"

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response, unsafe_allow_html=True)

                # --- Step 5: Show download button ---
                if result["ok"]:
                    st.download_button(
                        label="📥 Download Test Cases (Markdown)",
                        data=response,
                        file_name=f"test_cases_{issue_key}.md",
                        mime="text/markdown",
                    )