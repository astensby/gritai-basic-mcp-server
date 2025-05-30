import json
import random
import uuid
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("HelloServer")


# Add a hello tool
@mcp.tool()
def hello() -> str:
    """Returns a hello message"""
    return "Hello from the MCP server!"

# Tool to get a random motivational quote
@mcp.tool()
def get_random_quote() -> str:
    """Reads from quotes.json and returns a random motivational quote."""
    try:
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
        if not quotes:
            return "No quotes found in quotes.json."
        random_quote = random.choice(quotes)
        return f'"{random_quote["quote"]}" - {random_quote["author"]}'
    except FileNotFoundError:
        return "Error: quotes.json not found."
    except json.JSONDecodeError:
        return "Error: quotes.json is not a valid JSON file."
    except (TypeError, KeyError):
        return "Error: quotes.json does not have the expected format (list of objects with 'quote' and 'author' keys)."

# --- Task Manager ---
TASKS_FILE = "tasks.json"

def _load_tasks() -> List[Dict[str, Any]]:
    try:
        with open(TASKS_FILE, "r") as f:
            tasks = json.load(f)
            if not isinstance(tasks, list): # Ensure it's a list
                return []
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_tasks(tasks: List[Dict[str, Any]]) -> None:
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@mcp.tool()
def add_task(description: str) -> Dict[str, Any]:
    """Adds a new task to the task list."""
    if not description or not description.strip():
        return {"error": "Task description cannot be empty."}
    tasks = _load_tasks()
    new_task = {
        "id": str(uuid.uuid4()),
        "description": description,
        "status": "pending" # 'pending' or 'complete'
    }
    tasks.append(new_task)
    _save_tasks(tasks)
    return new_task

@mcp.tool()
def list_tasks(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lists tasks. Can be filtered by status: 'pending' or 'complete'."""
    tasks = _load_tasks()
    if not tasks:
        return []
    if status_filter:
        if status_filter not in ["pending", "complete"]:
            # Return an empty list or an error message if the filter is invalid
            # For simplicity, returning filtered list which might be empty
            return [task for task in tasks if task.get("status") == "invalid_filter_value_intentionally"]
        return [task for task in tasks if task.get("status") == status_filter]
    return tasks

@mcp.tool()
def mark_task_complete(task_id: str) -> Dict[str, Any]:
    """Marks a task as complete by its ID."""
    if not task_id or not task_id.strip():
        return {"error": "Task ID cannot be empty."}
    tasks = _load_tasks()
    task_found = False
    for task in tasks:
        if task.get("id") == task_id:
            if task.get("status") == "complete":
                return {"message": f"Task '{task_id}' is already complete.", "task": task}
            task["status"] = "complete"
            task_found = True
            break
    if not task_found:
        return {"error": f"Task with ID '{task_id}' not found."}
    _save_tasks(tasks)
    # Return the updated task
    updated_task = next((task for task in tasks if task.get("id") == task_id), None)
    return updated_task if updated_task else {"error": "Failed to retrieve updated task, but operation might have succeeded."}


def main():
    """Runs the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main() 