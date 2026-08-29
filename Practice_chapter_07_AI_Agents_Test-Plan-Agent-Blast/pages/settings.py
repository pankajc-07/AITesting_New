"""Settings page for the Test Plan Agent."""
import streamlit as st
from tools import config_store
from tools.errors import AgentError

st.set_page_config(page_title="Settings - Test Plan Agent", page_icon="⚙️")

st.title("⚙️ Settings")
st.caption("Configure Jira and Groq connections.")

cfg = config_store.load_config()

# --- Jira Settings ---
st.subheader("🔗 Jira Connection")
col1, col2 = st.columns([3, 1])
with col1:
    jira_url = st.text_input("Jira URL", value=cfg.get("jira_url", ""),
                             placeholder="https://your-company.atlassian.net")
    jira_email = st.text_input("Jira Email", value=cfg.get("jira_email", ""),
                               placeholder="you@company.com")
    jira_token = st.text_input("Jira API Token", value=cfg.get("jira_api_token", ""),
                               type="password",
                               placeholder="Paste from id.atlassian.com")
with col2:
    st.caption("")
    if st.button("Test Jira Connection", use_container_width=True):
        # Save temporarily for the test
        config_store.save_config({
            "jira_url": jira_url,
            "jira_email": jira_email,
            "jira_api_token": jira_token,
        })
        try:
            from tools import jira_auth
            info = jira_auth.verify()
            st.success(f"✅ Connected as **{info.get('displayName', '?')}** "
                      f"({info.get('emailAddress', '?')})")
        except AgentError as e:
            st.error(f"❌ {e.message}\n\n{e.remedy}")

# --- Groq Settings ---
st.subheader("🤖 Groq LLM Connection")
col1, col2 = st.columns([3, 1])
with col1:
    groq_key = st.text_input("Groq API Key", value=cfg.get("groq_api_key", ""),
                             type="password",
                             placeholder="gsk_... from console.groq.com/keys")
    groq_model = st.text_input("Groq Model", value=cfg.get("groq_model", "openai/gpt-oss-120b"),
                               placeholder="openai/gpt-oss-120b")
with col2:
    st.caption("")
    if st.button("Test Groq Connection", use_container_width=True):
        config_store.save_config({
            "groq_api_key": groq_key,
            "groq_model": groq_model,
        })
        try:
            from tools import llm_client
            info = llm_client.verify()
            st.success(f"✅ Connected! Model: **{info.get('model', '?')}** "
                      f"on **{info.get('provider', '?')}**")
        except AgentError as e:
            st.error(f"❌ {e.message}\n\n{e.remedy}")

# --- Save Section ---
st.divider()
st.subheader("💾 Save Settings")
default_key = st.text_input("Default Jira Key", value=cfg.get("default_jira_key", "PROJ-1"),
                            placeholder="PROJ-1")

if st.button("Save All Settings", type="primary"):
    config_store.save_config({
        "jira_url": jira_url,
        "jira_email": jira_email,
        "jira_api_token": jira_token,
        "groq_api_key": groq_key,
        "groq_model": groq_model,
        "llm_provider": "groq",
        "default_jira_key": default_key,
    })
    st.success("✅ All settings saved!")
    st.rerun()

st.divider()
st.caption("API Token: [id.atlassian.com](https://id.atlassian.com/manage-profile/security/api-tokens) | "
           "Groq Key: [console.groq.com/keys](https://console.groq.com/keys)")