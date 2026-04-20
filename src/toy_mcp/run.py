# this is the main entry point for the application
from mcp.server.fastmcp import FastMCP
import requests

session = requests.Session() # create a session to reuse connections
tasks = [] # simple in-memory task list

# toy server with fastMCP


# Create a server instance
mcp = FastMCP("HelloWorld", log_level="DEBUG")

# Hello World Tools
@mcp.tool()
def say_hello(name: str = "World") -> str:
    """Return a greeting message to the specified name (defaults to 'World')."""
    return f"Hello, {name}!"

@mcp.tool()
def say_goodbye(name: str = "World") -> str:
    """Return a goodbye message to the specified name (defaults to 'World')."""
    return f"Goodbye, {name}!"

# Math Tools
@mcp.tool()
def math_double(a: int) -> int:
    """Return the input integer multiplied by 2."""
    return a * 2

# Stateful Tools
@mcp.tool()
def add_task(task: str) -> str:
    """Add a new task (string) to the in-memory task list."""
    tasks.append(task)
    return "Task added."

@mcp.tool()
def list_tasks() -> str:
    """Return all tasks as a newline-separated string, or a message if no tasks exist."""
    if tasks:
        return "\n".join(tasks) # I think claude ai or FastMCP doesnt return the list well and it comes out as a together string if i return tasks (e.g. "Task1Task2Task3")
    else:
        return "No tasks found."

@mcp.tool()
def count_tasks() -> int:
    """Return the total number of tasks currently stored."""
    return len(tasks)

@mcp.tool()
def clear_task(task: str = None, taskIdx: int = -1) -> str:
    """
    Remove a task either by its exact name or by its 0-based index (provide only one).
    taskIdx is a 0-indexed identifer for what task you want to be cleared in the list
    task is the string of the task you want to be cleared
    """

    if taskIdx == -1 and task == None: # no input provided
        return "please provide either a task or a index"
    elif taskIdx != -1 and task != None: # both inputs provided
        return "please provide either a task or a index, not both"
    elif taskIdx != -1: # index provided
        return index_clear_task(taskIdx)
    elif task is not None and task in tasks:
        return string_clear_task(task)
    else:
        return "task not found, please provide a valid task to clear"

def index_clear_task(taskIdx: int) -> str:
    if 0 <= taskIdx < len(tasks):
        tasks.pop(taskIdx)
        return "Task cleared by index"
    else:
        return "invalid index provided, please provide a valid index"

def string_clear_task(task: str) -> str:
    if task in tasks:
        tasks.remove(task)
        return "Task cleared by name"
    else:
        return "task not found, please provide a valid task to clear"

@mcp.tool()
def count_words(text: str) -> int:
    """Return the number of words in the given text (split by whitespace)."""
    return len(text.split())

# Weather API Tools
def request_weather_data(longitude: float = 13.41, latitude: float = 52.52) -> dict:
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    try:
        response = session.get(api_url, timeout=5)

        if response.ok:  # checks if response is successful (status code 200-299)
            return response.json()
        else:
            return {"error": f"API returned status {response.status_code}"}

    except requests.RequestException as e:
        return {"error": str(e)} # returns a error message so can be handled by the client (Claude AI)


@mcp.tool()
def get_weather(longitude: float, latitude: float) -> dict:
    """Fetch current and hourly weather data for the given latitude and longitude using the Open-Meteo API."""
    if not (-180 <= longitude <= 180 and -90 <= latitude <= 90): # verify that the coordinates are valid before making API request
        return {"error": "Invalid coordinates"}
    
    return request_weather_data(longitude, latitude) # return the weather data as a dictionary


# uv
def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()