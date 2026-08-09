"""
Settings page for Jira Test Case Generator.

Configure Jira connection, LLM provider, and API keys.
Settings are persisted to settings.json via config_store.
"""

import streamlit as st
import sys
from pathlib import Path

# Ensure src/ is on sys.path so we can import sibling modules
SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config_store import load_settings, save_settings

st.set_page_config(page_title="Settings — Jira TC Generator", page_icon="⚙️")

st.title("⚙️ Settings")
st.caption("Configure your Jira connection and LLM provider. Settings are saved locally.")

# ---------------------------------------------------------------------------
# Load current settings
# ---------------------------------------------------------------------------
settings = load_settings()

# ---------------------------------------------------------------------------
# Helper: build settings dict from current form values
# ---------------------------------------------------------------------------
def _collect_form_values():
    return {
        "JIRA_BASE_URL": st.session_state.get("s_jira_url", "").strip(),
        "JIRA_EMAIL": st.session_state.get("s_jira_email", "").strip(),
        "JIRA_API_TOKEN": st.session_state.get("s_jira_token", "").strip(),
        "LLM_PROVIDER": st.session_state.get("s_provider", "ollama"),
        "GROQ_API_KEY": st.session_state.get("s_groq_key", "").strip(),
        "OLLAMA_BASE_URL": st.session_state.get("s_ollama_url", "http://localhost:11434").strip(),
        "OLLAMA_MODEL": st.session_state.get("s_ollama_model", "gemma3:1b").strip(),
    }

# ---------------------------------------------------------------------------
# Jira Configuration
# ---------------------------------------------------------------------------
st.subheader("🔗 Jira Connection")

st.text_input(
    "Jira Base URL",
    value=settings.get("JIRA_BASE_URL", ""),
    placeholder="https://your-company.atlassian.net",
    help="Your Jira Cloud or Server base URL.",
    key="s_jira_url",
)

col1, col2 = st.columns(2)
with col1:
    st.text_input(
        "Jira Email",
        value=settings.get("JIRA_EMAIL", ""),
        placeholder="you@company.com",
        key="s_jira_email",
    )
with col2:
    st.text_input(
        "Jira API Token",
        value=settings.get("JIRA_API_TOKEN", ""),
        type="password",
        placeholder="Your Jira API token",
        help="Generate at https://id.atlassian.com/manage-profile/security/api-tokens",
        key="s_jira_token",
    )

# ---------------------------------------------------------------------------
# LLM Provider
# ---------------------------------------------------------------------------
st.subheader("🤖 LLM Provider")

st.selectbox(
    "Default Provider",
    options=["ollama", "groq"],
    index=0 if settings.get("LLM_PROVIDER", "ollama") == "ollama" else 1,
    help="Ollama = local (free, private). Groq = cloud (fast, requires API key).",
    key="s_provider",
)

# Show Groq key only when Groq is selected
if st.session_state.get("s_provider", "ollama") == "groq":
    st.text_input(
        "Groq API Key",
        value=settings.get("GROQ_API_KEY", ""),
        type="password",
        placeholder="gsk_...",
        help="Get your key at https://console.groq.com/keys",
        key="s_groq_key",
    )
else:
    st.session_state["s_groq_key"] = settings.get("GROQ_API_KEY", "")

# Ollama advanced settings (collapsed by default)
with st.expander("🦙 Ollama Advanced"):
    st.text_input(
        "Ollama Base URL",
        value=settings.get("OLLAMA_BASE_URL", "http://localhost:11434"),
        key="s_ollama_url",
    )
    st.text_input(
        "Model",
        value=settings.get("OLLAMA_MODEL", "gemma3:1b"),
        key="s_ollama_model",
    )

# ---------------------------------------------------------------------------
# Save button
# ---------------------------------------------------------------------------
st.divider()

if st.button("💾 Save Settings", type="primary", use_container_width=True):
    save_settings(_collect_form_values())
    st.success("✅ Settings saved successfully!")
    st.rerun()

# ---------------------------------------------------------------------------
# Test Connection buttons
# ---------------------------------------------------------------------------
st.subheader("🔍 Test Connections")

col_a, col_b = st.columns(2)

with col_a:
    if st.button("Test Jira Connection", use_container_width=True):
        vals = _collect_form_values()
        if not vals["JIRA_BASE_URL"] or not vals["JIRA_EMAIL"] or not vals["JIRA_API_TOKEN"]:
            st.error("Fill in Jira URL, Email, and API Token first.")
        else:
            save_settings(vals)
            from jira_client import fetch_issue
            with st.spinner("Connecting to Jira..."):
                result = fetch_issue("TEST-1")
            if result["ok"]:
                st.success("✅ Jira connected! (TEST-1 may not exist, but auth works)")
            else:
                st.error(f"❌ {result['error']}")

with col_b:
    if st.button("Test LLM Connection", use_container_width=True):
        vals = _collect_form_values()
        save_settings(vals)
        from llm_client import generate_test_cases
        with st.spinner(f"Testing {vals['LLM_PROVIDER'].upper()}..."):
            result = generate_test_cases("Reply with exactly: OK", provider=vals["LLM_PROVIDER"])
        if result["ok"]:
            st.success(f"✅ {result['provider']} responded!")
        else:
            st.error(f"❌ {result['error']}")