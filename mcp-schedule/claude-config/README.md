This guide provides detailed instructions for setting up and configuring Claude AI integration with the MCP Server platform using Claude Desktop.

## Overview

The Claude integration enables natural language processing capabilities for the MCP Server, particularly enhancing the human-readable scheduling expressions in the MCP Schedule Server component.

## Prerequisites

- Claude Desktop application installed
- Python 3.8+
- MCP Server base installation

## Setting Up Claude Desktop

1. **Download and Install Claude Desktop**
   - Visit the [Anthropic website](https://www.anthropic.com/claude) to download Claude Desktop
   - Follow the installation wizard instructions for your operating system

2. **Configure Claude Desktop**
   - Launch Claude Desktop
   - Navigate to Settings (gear icon)
   - Select "API Access"
   - Enter your API key
   - Click "Save"

3. **Link Claude Desktop to MCP Server**
   - In Claude Desktop, go to "Integrations"
   - Select "External Applications"
   - Click "Add New Integration"
   - Enter the following details:
     - Name: MCP Server
     - Endpoint URL: http://localhost:8428/claude
   - Click "Test Connection" to verify
   - Click "Save"

## Configure with JSON

Add this to `claude_desktop_config_sample.json`. 

You can open it by selecting in Claude Desktop the `File / Settings / Developer / Edit Config` menus / buttons. 

```json
{
  "mcpServers": {
    "mcp-schedule": {
      "command": "uvicorn",
      "args": [
        "mcp_schedule_server:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8428"
      ]
    }
  },
  "toolSchemas": [
    "./claude_tools_mcp_schedule.json"
  ]
}
```
## Then Copy
You need to copy [`claude_tools_mcp_schedule.json`](claude_tools_mcp_schedule.json) into the same folder where your `claude_desktop_config_sample.json` exists.



## Usage with MCP Schedule Server

Once configured, the Claude integration enhances the `parse_human_to_cron` function in the MCP Schedule Server:

1. **Using the CLI**:

```bash
python mcp_schedule_server.py add "every weekday morning at 8:30" "send-notification 'Morning meeting'"
```

2. **Using the API**:

```bash
curl -X POST http://localhost:8428/schedule \
  -H "Content-Type: application/json" \
  -d '{"expression": "first Monday of each month at noon", "command": "generate-monthly-report"}'
```

## Advanced Configuration

### Custom Prompts

You can create custom system prompts for specific scheduling scenarios by creating a `prompts` directory:

```bash
mkdir -p claude-config/prompts
```

Add your custom prompt files (e.g., `scheduling_prompt.txt`) and reference them in your configuration.

### Integration with Other MCP Components

To enable Claude capabilities in other MCP components:

1. Import the Claude client:

```python
from claude_config.client import claude_client
```

2. Use the client in your component:

```python
response = claude_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Parse this: every other Friday"}]
)
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify your API key is correct
   - Check your internet connection
   - Ensure you're not exceeding API rate limits

2. **Integration Issues**
   - Restart Claude Desktop
   - Verify the endpoint URL is correct
   - Check MCP Server logs for connection errors

3. **Parsing Errors**
   - Review the system prompt for clarity
   - Consider using a more capable Claude model
   - Add examples to the system prompt for better context

## Resources

- [Anthropic API Documentation](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [Claude Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
- [Crontab Expression Reference](https://crontab.guru/)

## Other methods

# Claude Configuration Files for MCP Schedule Server

The `claude-config` directory contains two JSON files that serve different but complementary purposes in integrating Claude AI with the MCP Schedule Server. These files enable Claude Desktop to interact with your scheduling system through a well-defined interface.

## File Purposes

### 1. claude_desktop_config_sample.json

This file serves as a configuration template for Claude Desktop, defining how the application should connect to and interact with the MCP Schedule Server. It contains:

- Authentication settings
- API endpoint configurations
- Connection parameters
- User interface preferences

This is a sample configuration file that users should copy and customize for their specific environment.

### 2. claude_tools_mcp_schedule.json

This file defines the Claude Tools API schema that enables Claude to interact with the MCP Schedule Server. It follows the Claude Tools specification format and provides:

- Tool definitions for scheduling operations
- Input schemas for each operation
- API endpoint mappings
- Parameter descriptions and validation rules

This file enables Claude to understand how to properly format requests to the MCP Schedule Server API.

## How These Files Work Together

When properly configured:

1. Claude Desktop loads the configuration from `claude_desktop_config_sample.json` (renamed to your actual config)
2. The Tools API schema from `claude_tools_mcp_schedule.json` is registered with Claude
3. Users can then interact with Claude using natural language to schedule jobs
4. Claude uses the Tools API schema to translate user requests into properly formatted API calls
5. The MCP Schedule Server receives and processes these API calls

## Setting Up Claude Desktop with These Files

### Step 1: Configure Claude Desktop

1. Install Claude Desktop from the [Anthropic website](https://www.anthropic.com/claude)

2. Copy the sample configuration file:
   ```bash
   cp claude_desktop_config_sample.json claude_desktop_config.json
   ```

3. Edit `claude_desktop_config.json` to include your specific settings:
   - Set the correct server URL (default is http://localhost:8428)

4. In Claude Desktop:
   - Go to Settings → Advanced
   - Click "Import Configuration"
   - Select your edited `claude_desktop_config.json` file
   - Restart Claude Desktop when prompted

### Step 2: Register the Tools API

1. In Claude Desktop:
   - Go to Settings → Tools
   - Click "Register New Tool"
   - Select the `claude_tools_mcp_schedule.json` file
   - Verify the tool appears in the "Registered Tools" list

2. Test the connection:
   - In the Claude chat interface, type: "Can you help me schedule a job to run every day at 10pm?"
   - Claude should recognize this as a scheduling request and use the appropriate tool
   - It will format the API call to the MCP Schedule Server based on the schema

### Step 3: Using the Tools

Once configured, you can use natural language to:

1. **Schedule jobs** - "Schedule a backup script to run every Tuesday at 3am"
2. **List existing jobs** - "Show me all my scheduled jobs"
3. **Delete jobs** - "Remove the backup job that runs on Tuesdays"

Claude will translate these requests into the appropriate API calls using the schema defined in `claude_tools_mcp_schedule.json`.

## Troubleshooting

- **Connection Issues**: Verify the server URL in your configuration file and ensure the MCP Schedule Server is running
- **Authentication Errors**: Check that any required API keys or tokens are correctly set in your configuration
- **Schema Errors**: If Claude fails to properly format requests, verify the `claude_tools_mcp_schedule.json` file matches your server's API specification

## Advanced Configuration

You can customize the `claude_tools_mcp_schedule.json` file to:

- Add new tools for additional server functionality
- Enhance descriptions to improve Claude's understanding
- Add examples to guide Claude's usage of the tools
- Modify input schemas to match changes in your API

Remember to re-register the tools in Claude Desktop after making changes to the schema file.

---
