# mcp-server

A modular server framework for various MCP (Model Context Protocol) services.

## Components

### [MCP Schedule Server](./mcp-schedule/README.md)

A minimalist crontab management server and CLI tool built with FastAPI, Typer, and Pydantic v2. Provides human-friendly scheduling expressions and native crontab syntax support.

- Parse human or crontab syntax (`"every day at 5pm"` → `0 17 * * *`)
- Persist cron entries via `crontab` interface
- FastAPI server with switchable transport: stdio or SSE
- CLI support using `typer`

### [Claude Configuration](./mcp-schedule/claude-config/README.md)

Integration with Claude AI to enhance natural language processing capabilities:

- Convert complex human-readable scheduling expressions to crontab syntax
- Claude Desktop integration via Tools API
- Custom prompt templates for scheduling scenarios

## Project Structure

```
mcp-server/
├── mcp-schedule/             # Crontab management service
│   ├── mcp_schedule_server.py  # Main server and CLI implementation
│   ├── requirements.txt        # Python dependencies
│   ├── README.md               # Component documentation
│   └── claude-config/          # Claude AI integration
│       ├── claude_desktop_config_sample.json  # Claude Desktop configuration
│       ├── claude_tools_mcp_schedule.json     # Claude Tools API schema
│       └── README.md           # Claude integration documentation
├── README.md                 # This file
└── ...                       # Other MCP components (future)
```

## Getting Started

Each component has its own installation and usage instructions. Navigate to the respective component directory and follow the instructions in its README.

For example, to use the MCP Schedule Server:

```bash
cd mcp-schedule
pip install -r requirements.txt
python mcp_schedule_server.py --help
```

To set up Claude integration:

```bash
cd mcp-schedule/claude-config
# Follow the instructions in README.md to configure Claude Desktop
```

## Architecture

The MCP Server is designed as a collection of modular services that can be deployed independently or together. Each service follows these design principles:

- RESTful API design with FastAPI
- Strong type validation with Pydantic
- CLI interface with Typer
- Rich terminal output formatting
- Environment-configurable behavior
- AI integration capabilities

## Development

### Prerequisites

- Python 3.8+
- Required system packages (varies by component)
- Claude Desktop (optional, for AI integration)

### Contributing

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[MIT](LICENSE) (or follow the upstream licenses of the references in requirements.txt and pyproject.toml files)
