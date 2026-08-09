"""
llm_client.py — LLM orchestrator with Ollama (local) → Groq (cloud) fallback.

Default: Ollama at http://localhost:11434, model gemma3:1b.
Fallback: Groq API (llama-3.1-8b-instant) when Ollama is unreachable
          or the user explicitly selects Groq in Settings.
"""

import requests
from config_store import get_setting


# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------

def _call_ollama(prompt: str) -> str:
    """Send a prompt to the local Ollama server.  Raises on failure."""
    base_url = get_setting("OLLAMA_BASE_URL", "http://localhost:11434")
    model = get_setting("OLLAMA_MODEL", "gemma3:1b")

    resp = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")


# ---------------------------------------------------------------------------
# Groq
# ---------------------------------------------------------------------------

def _call_groq(prompt: str) -> str:
    """Send a prompt to Groq Cloud.  Raises on failure."""
    from groq import Groq

    api_key = get_setting("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("Groq API key is not configured. Go to Settings.")

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2048,
    )
    return completion.choices[0].message.content or ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_test_cases(prompt: str, provider: str | None = None) -> dict:
    """
    Generate test cases using the configured LLM.

    Parameters
    ----------
    prompt : str
        The filled-in prompt template ready for the LLM.
    provider : str | None
        "ollama", "groq", or None (auto-detect from settings).

    Returns
    -------
    dict with keys:
        ok      : bool
        response: str   (the generated text, if ok)
        provider: str   ("ollama" or "groq")
        error   : str   (human-readable, if not ok)
    """
    if provider is None:
        provider = get_setting("LLM_PROVIDER", "ollama")

    # --- Explicit Groq ---
    if provider == "groq":
        try:
            text = _call_groq(prompt)
            return {"ok": True, "response": text, "provider": "groq"}
        except Exception as exc:
            return {"ok": False, "error": f"Groq API error: {exc}", "provider": "groq"}

    # --- Ollama (with fallback to Groq) ---
    try:
        text = _call_ollama(prompt)
        return {"ok": True, "response": text, "provider": "ollama"}
    except requests.exceptions.ConnectionError:
        pass  # Ollama not running → try Groq
    except requests.exceptions.Timeout:
        pass  # Ollama timed out → try Groq
    except Exception:
        pass  # Any other Ollama error → try Groq

    # --- Fallback to Groq ---
    try:
        text = _call_groq(prompt)
        return {"ok": True, "response": text, "provider": "groq (fallback)"}
    except Exception as exc:
        return {
            "ok": False,
            "error": (
                f"Ollama is unreachable and Groq fallback also failed: {exc}\n\n"
                "Make sure Ollama is running (`ollama serve`) or configure a valid Groq API key in Settings."
            ),
            "provider": "none",
        }


# ---------------------------------------------------------------------------
# Standalone smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result = generate_test_cases("Say hello in exactly 5 words.")
    print(f"Provider: {result.get('provider')}")
    print(f"OK: {result.get('ok')}")
    print(f"Response: {result.get('response', result.get('error'))[:300]}")