# LLM Usage

The candidate detector optionally calls OpenAI when `OPENAI_API_KEY` is set; otherwise it uses the deterministic fallback. The model is asked only to propose labels, descriptions, ranges, and source IDs drawn from the supplied window. It is not a source of truth.

Invalid coordinates and evidence IDs outside the window are discarded. The provenance validator independently checks page/line existence, range ordering, non-empty text, and evidence text matching. API keys are read from environment variables and `.env` remains ignored.
