"""LLM client. OpenAI-compatible REST via `requests`. Provider: Groq.

AI-2: this is the ONLY module in the project permitted to call a model.
"""
import requests

from tools.config_store import load_config
from tools.errors import ConfigError, LLMError

TIMEOUT = 120

PROVIDERS = {
    "groq": {
        "label": "Groq",
        "base": "https://api.groq.com/openai/v1",
        "key_setting": "groq_api_key",
        "model_setting": "groq_model",
        "default_model": "openai/gpt-oss-120b",
        "tpm": 8000,
        "console": "console.groq.com/keys",
    },
}


def provider_spec(name=None):
    cfg = load_config()
    name = (name or cfg.get("llm_provider") or "groq").lower()
    if name not in PROVIDERS:
        raise ConfigError(
            "Unknown LLM provider: " + repr(name),
            "Pick one of: " + ", ".join(PROVIDERS),
        )
    result = {"name": name}
    result.update(PROVIDERS[name])
    return result


def _key_and_model():
    cfg = load_config()
    spec = provider_spec()
    key = cfg.get(spec["key_setting"])
    if not key:
        raise ConfigError(
            spec["label"] + " API key is not configured.",
            "Open the Settings page and paste your key from " + spec["console"],
        )
    model = cfg.get(spec["model_setting"]) or spec["default_model"]
    return key, model, spec


def verify():
    """Phase 2 LINK handshake: prove the provider answers and the model exists."""
    key, model, spec = _key_and_model()
    try:
        resp = requests.get(
            spec["base"] + "/models",
            headers={"Authorization": "Bearer " + key},
            timeout=30,
        )
    except requests.exceptions.RequestException as e:
        raise LLMError(
            "Cannot reach " + spec["label"] + ": " + str(e),
            "Check your network connection.",
        )

    if resp.status_code == 401:
        raise LLMError(
            spec["label"] + " rejected the API key (401).",
            "Generate a new key at " + spec["console"] + " and update Settings.",
        )
    if not resp.ok:
        raise LLMError(
            spec["label"] + " error " + str(resp.status_code) + ": " + resp.text[:200],
            "Check Settings.",
        )

    return {"model": model, "provider": spec["label"]}


def chat(messages, temperature=0.3, max_tokens=4096, response_format=None):
    """Send a chat completion request. Returns the full API response.

    Args:
        messages: OpenAI-format message list.
        temperature: 0.0-2.0. Pinned at 0.3 to reduce hallucination (BR-8).
        max_tokens: Max tokens in response.
        response_format: Optional {"type": "json_object"}.
    """
    key, model, spec = _key_and_model()

    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if response_format:
        body["response_format"] = response_format

    try:
        resp = requests.post(
            spec["base"] + "/chat/completions",
            headers={
                "Authorization": "Bearer " + key,
                "Content-Type": "application/json",
            },
            json=body,
            timeout=TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        raise LLMError(
            spec["label"] + " request failed: " + str(e),
            "Check your network and retry.",
        )

    if resp.status_code == 401:
        raise LLMError(
            spec["label"] + " rejected the API key (401).",
            "Generate a new key at " + spec["console"] + ".",
        )
    if resp.status_code == 429:
        raise LLMError(
            spec["label"] + " rate limit hit (429).",
            "Wait a minute and retry, or upgrade your plan.",
        )
    if resp.status_code == 413:
        raise LLMError(
            "Prompt too large for the model context window.",
            "The ticket description is very large. Try a shorter ticket.",
        )
    if not resp.ok:
        raise LLMError(
            spec["label"] + " returned " + str(resp.status_code) + ": " + resp.text[:300],
            "Check the API key and model name in Settings.",
        )

    return resp.json()