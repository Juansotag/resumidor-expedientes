import traceback
try:
    from duckduckgo_search import DDGS
    res = list(DDGS().text("test", max_results=3))
    print("DDG OK:", res)
except Exception as e:
    print("DDG FAILED:", str(e))
    traceback.print_exc()

import anthropic
import os
try:
    client = anthropic.Anthropic(api_key="test_fake_key")
    client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=10,
        messages=[{"role": "user", "content": "hello"}]
    )
except Exception as e:
    print("Anthropic FAILED:", str(e))
    # traceback.print_exc()
