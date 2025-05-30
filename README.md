# Beginner's Guide to MCP Servers

A simple demonstration project to help beginners understand and build Model Context Protocol (MCP) servers with minimal coding experience.

## What is MCP?

Model Context Protocol (MCP) is a way for AI assistants (like Claude, ChatGPT, etc.) to connect to external tools and data sources. Think of it as a bridge that allows AI to:
- Fetch real-time information from the internet
- Interact with your local files and applications
- Perform specific tasks on your behalf

This project contains two example MCP servers that demonstrate different types of functionality.

## What's Included

This project includes two MCP servers:

### 1. Motivational Quotes & Task Manager Server (`motivational_server.py`)
Demonstrates local file operations and task management:
- **Hello Tool**: A simple greeting function
- **Random Quotes**: Gets motivational quotes from a local JSON file
- **Task Manager**: Add, list, and complete tasks stored locally


### 1. Any API Server (`server.py`)
Demonstrates connecting to external APIs:
- **Norwegian Police Incidents**: Fetches real-time police incidents from Norway's public API
- **Stock Market Tools**: Search for company stock tickers and get current stock prices (requires a free Alpha Vantage API key)


## Prerequisites

Before you start, make sure you have:
- Python 3.11 or higher installed on your computer

## Installation & Setup

### Step 1: Clone or Download This Project
Download this project to your computer and navigate to the project folder in your terminal.

### Step 2: Create a Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -e .
```

### Step 5: (Optional) Set Up Stock Market API
To use the stock market features, you'll need a free API key from Alpha Vantage:
1. Go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and get a free API key
2. Set it as an environment variable:
   ```bash
   export ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```

## How to Use With AI Assistants

### With Claude Desktop
1. Open your Claude Desktop configuration file
2. Add the server configuration:
```json
{
  "mcpServers": {
    "HelloServer": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "--directory",
        "/path/to/your/project",
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "server.py"        
      ],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "demo"
      }
    }
  }
}
```

### With Other MCP Clients
Refer to your MCP client's documentation for connection instructions.

## Available Tools

### Main Server Tools
- `hello()` - Returns a greeting message
- `get_police_incidents()` - Fetches latest police incidents from Norway
- `get_incidents_by_district(district_name)` - Get incidents from a specific police district
- `get_incidents_by_municipality(municipality_name)` - Get incidents from a specific municipality
- `search_stock_ticker(company_name)` - Search for a company's stock ticker symbol
- `get_stock_price(symbol)` - Get current stock price for a ticker symbol

### Motivational Server Tools
- `hello()` - Returns a greeting message
- `get_random_quote()` - Returns a random motivational quote
- `add_task(description)` - Adds a new task to your task list
- `list_tasks(status_filter)` - Lists tasks (optionally filter by "pending" or "complete")
- `mark_task_complete(task_id)` - Marks a task as complete

## Project Structure

```
gritai-basic-mcp-server/
├── server.py              # Main server with API integrations
├── motivational_server.py # Server with local file operations
├── quotes.json           # Motivational quotes database
├── tasks.json            # Task storage file
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## Customizing the Servers

### Adding New Quotes
Edit `quotes.json` to add your own motivational quotes:
```json
{
  "quote": "Your inspiring quote here",
  "author": "Quote Author"
}
```

### Adding New Tools
To add a new tool to either server, use the `@mcp.tool()` decorator:
```python
@mcp.tool()
def your_new_tool(parameter: str) -> str:
    """Description of what your tool does."""
    # Your tool logic here
    return "Result"
```

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Make sure you've activated your virtual environment
- Run `pip install -e .` to install dependencies

**API errors for stock tools**
- Check that your Alpha Vantage API key is set correctly
- Free API keys have rate limits

**File not found errors**
- Make sure you're running the server from the project directory
- Check that `quotes.json` and `tasks.json` exist

### Getting Help
- Check the [MCP documentation](https://modelcontextprotocol.io/)
- Review the code comments for implementation details
- The servers include error handling to help identify issues

## Next Steps

Once you're comfortable with these examples:
1. Try modifying the existing tools
2. Add your own API integrations
3. Create tools that interact with your local files
4. Explore the MCP specification to understand advanced features