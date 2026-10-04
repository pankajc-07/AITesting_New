# Putting a self-hosted RAG on a public static host

**Problem:** QABuddy (chapter 12) needs Qdrant, Ollama (Qwen3-Embedding-4B), a GPU
cross-encoder reranker and a rate-limited LLM. It had to become a public Vercel demo that
people can actually use, without misrepresenting what the real system does.

## Approach

1. **Two honest paths, no fake backend.**
   - Example questions: run each through the FULL local pipeline and record every event
     (dense/BM25/RRF ranks, rerank scores, selection reasons, answer, citations, timings).
     The browser replays them, keyed by `mode::normalized question`.
   - Free-text questions: port the BM25 tokenizer to JS (camelCase split, ids like
     `VWO-26` kept whole, stopwords, light stemmer) and run BM25 in the browser over an
     exported `corpus.json`. Send the top chunks to a small serverless function that calls
     the LLM. Generate its system prompt from the Python source so the two never drift.
     Label these answers "BM25 in browser" in the UI.
2. **Parity test across languages.** A pytest case shells out to node and compares token
   streams on tricky inputs. Without it the two tokenizers drift silently.
3. **Record under the rate limit.** Groq on-demand allows 8k tokens/minute and counts the
   `max_tokens` reservation. Back-to-back recordings queued behind 429s, which pushed the
   recorded first-token time to 13-28 s. Pace the recordings 32 s apart, and report the
   rate-limit wait as its own timing field, kept out of the latency numbers.
4. **Audit every recording before shipping.** Each one must be cited, grounded and free of
   rate-limit waits. If an example legitimately refuses, swap the example, not the
   answer. "Map login requirements" refused because the PRD has none.
5. **Scan what the demo serves for secrets.** `corpus.json` is the whole index, and anyone
   can download it.
6. **Verify the deployed URL in a real browser**, not just with curl:
   - a recorded example replays
   - a free-text question round-trips through the function
   - the console is clean

## Judgment calls (what was NOT done)

- **No tunnel from the public page to the laptop backend** (chapter 09 used cloudflared).
  It would expose an index of code, tickets and logs, and the demo dies when the laptop
  sleeps.
- **No in-browser embedding model for free text** (chapter 10 used MiniLM). A different
  model ranks differently from the real system. Keyword search is an honest subset.
- **Root-cause fixes for deploy gotchas, not workarounds:**
  - Vercel picks a framework preset from the project root (`requirements.txt` with
    fastapi meant FastAPI), even when `.vercelignore` excludes that file. Fix: pin
    `"framework": null`.
  - The demo and self-hosted builds shared `ui/dist`, and `run.sh up` skipped building
    when `ui/dist/index.html` existed. So the self-hosted app silently came up replaying
    recordings. Fix: give the demo its own `outDir` (`ui/dist-demo`) rather than adding
    "is this a demo build?" detection.

## Reusable rule

To demo a self-hosted AI system publicly, replay recorded runs of the real pipeline and
run only a clearly labelled subset live. The demo must never share an output folder, a
framework preset, or a timing number with the real system.
