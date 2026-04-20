# MCP Toy Server

This is a simple Model Context Protocol (MCP) server built using FastMCP. It showcases basic tool creation, state management, and external API integration.

## Features

* **Hello World Tools**

  * `say_hello(name)`
  * `say_goodbye(name)`

* **Math Tool**

  * `math_double(a)` – returns `a * 2`

* **Task Management (Stateful)**

  * `add_task(task)` – add a task
  * `list_tasks()` – list all tasks
  * `count_tasks()` – count total tasks
  * `clear_task(task or taskIdx)` – remove a task by name or index

* **Text Tool**

  * `count_words(text)` – counts words in input text

* **Weather Tool**

  * `get_weather(longitude, latitude)` – fetches weather data from Open-Meteo API

## How It Works

* Uses an in-memory list (`tasks`) for simple state management
* Runs locally using MCP over `stdio`
* Reuses HTTP connections with a global `requests.Session`

### 1. Running the Server (uv)

```bash
uv sync
```

then

```bash
uv run toy-mcp
```

The server will start using stdio transport and can be used with an MCP-compatible client.


## Using with Claude Desktop

Alternatively, you can connect ```toy-mcp``` to your Claude Desktop MCP configuration to use the tools directly in chat.

To connect this MCP server to Claude Desktop in a local development setup, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "toy-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/home/YOUR_USERNAME/path/to/ToyMCP", "toy-mcp"]
    }
  }
}
```

## Notes

* This is a **toy/demo project** (single-user, in-memory state)