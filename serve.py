"""Start the bot on $PORT (default 8080). One worker, because state lives in memory.

A Python launcher rather than a shell command, so it works however the host runs it
(Railway runs start commands without a shell, so "$PORT" arrived as literal text).
"""

import os

import uvicorn

if __name__ == "__main__":
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", "8080")), workers=1, timeout_keep_alive=75)
