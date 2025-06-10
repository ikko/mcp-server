# mcp-server

A modular server framework for managing and orchestrating various MCP (Mission Control Platform) services.

## Components

### [MCP Schedule Server](./mcp-schedule/README.md)

A minimalist crontab management server and CLI tool built with FastAPI, Typer, and Pydantic v2. Provides human-friendly scheduling expressions and native crontab syntax support.

- Parse human or crontab syntax (`"every day at 5pm"` → `0 17 * * *`)
- Persist cron entries via `crontab` interface
- FastAPI server with switchable transport: stdio or SSE
- CLI support using `typer`

## Project Structure

```
mcp-server/
├── mcp-schedule/             # Crontab management service
│   ├── mcp_schedule_server.py  # Main server and CLI implementation
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Component documentation
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

## Architecture

The MCP Server is designed as a collection of modular services that can be deployed independently or together. Each service follows these design principles:

- RESTful API design with FastAPI
- Strong type validation with Pydantic
- CLI interface with Typer
- Rich terminal output formatting
- Environment-configurable behavior

## Development

### Prerequisites

- Python 3.8+
- Required system packages (varies by component)

### Contributing

1. Clone the repository
2. Install development dependencies
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT (or follow the upstream licenses of the references)
```

This README provides:

1. A clear introduction to the mcp-server project
2. A link to the mcp-schedule component with a brief description
3. The overall project structure
4. Getting started instructions
5. Architecture overview
6. Development prerequisites and contribution guidelines
7. License information

The structure is designed to be expandable as you add more components to the mcp-server project in the future. Each component can maintain its own detailed README while this main README serves as an entry point and overview of the entire system.
