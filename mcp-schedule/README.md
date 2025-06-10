# MCP Schedule Server

`mcp-schedule` is a minimalist crontab management server and CLI tool built with FastAPI, Typer, and Pydantic v2. It supports human-friendly scheduling expressions and native crontab syntax. Jobs are persisted in the system `crontab` (Ubuntu-compatible) and optionally filtered to only those managed by MCP.

## Features

* ✅ Parse human or crontab syntax (`"every day at 5pm"` → `0 17 * * *`)
* ✅ Persist cron entries via `crontab` interface
* ✅ FastAPI server with switchable transport: stdio or SSE
* ✅ CLI support using `typer`
* ✅ Rich output formatting in terminal
* ✅ Environment-configurable behavior via `.env` or env vars

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

You may also need to install `cron` system service:

```bash
sudo apt install cron
```

### 2. Create `.env` file (optional)

```ini
MCP_ONLY=true
TRANSPORT=stdio
```

### 3. Run the CLI

```bash
python mcp_schedule_server.py list

python mcp_schedule_server.py add "every day at 5pm" "/usr/bin/python3 /path/to/script.py"

python mcp_schedule_server.py add "0 8 * * 1-5" "notify-send 'Weekly Meeting'"
```

### 4. Run the API server

```bash
uvicorn mcp_schedule_server:app --reload
```

#### POST /schedule

```bash
curl -X POST http://localhost:8428/schedule \
  -H "Content-Type: application/json" \
  -d '{"expression": "every day at 5pm", "command": "echo hello"}'
```

#### GET /schedules

```bash
curl http://localhost:8428/schedules
```

If `TRANSPORT=sse`, use an SSE client like [curl with --no-buffer](https://curl.se/docs/manpage.html) or browser EventSource API.

---

## Project Structure

```
mcp-schedule/
├── mcp_schedule_server.py      # Main server and CLI file
├── .env                        # Optional environment settings
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Required Files

* `requirements.txt`

```
crontab
pydantic-settings
pydantic>=2.0
rich
fastapi
sse-starlette
typer
uvicorn
```

* `.env` (optional)

```ini
MCP_ONLY=true
TRANSPORT=sse
```

## Notes

* The job parsing logic includes a stub for human language to cron conversion. For production, integrate [Claude](https://www.claudemcp.com/servers/filesystem) or [OpenAI](https://platform.openai.com/docs/guides/gpt) with proper prompt templates.
* For crontab management, this uses the [python-crontab](https://pypi.org/project/crontab/) library.
* Jobs are marked with `# mcp` comment for filtering when `MCP_ONLY=true`.
* Ensure `cron` service is enabled:

```bash
sudo systemctl enable cron
sudo systemctl start cron
```

## License

MIT (or follow the upstream licenses of the references).
