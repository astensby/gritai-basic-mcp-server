import httpx
import os
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("HelloServer")


# Add a hello tool
@mcp.tool()
def hello() -> str:
    """Returns a hello message"""
    return "Hello from the MCP server!"


@mcp.tool()
def get_police_incidents() -> list[dict]:
    """Fetches the 10 latest incidents from the Norwegian Police API."""
    url = "https://api.politiet.no/politiloggen/v1/messages"
    headers = {"accept": "application/json"}  # Adjusted to accept JSON as per common practice for APIs returning JSON
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get("data", [])
    except httpx.HTTPStatusError as e:
        # Log or handle HTTP errors appropriately
        print(f"HTTP error occurred: {e}")
        return [{"error": "Failed to fetch incidents due to HTTP error", "details": str(e)}]
    except httpx.RequestError as e:
        # Log or handle other request errors (e.g., network issues)
        print(f"Request error occurred: {e}")
        return [{"error": "Failed to fetch incidents due to request error", "details": str(e)}]
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return [{"error": "An unexpected error occurred", "details": str(e)}]


@mcp.tool()
def get_incidents_by_district(district_name: str) -> list[dict]:
    """Fetches incidents from the Norwegian Police API filtered by a specific police district.
    
    Args:
        district_name (str): The name of the police district to filter by.

    Examples:
        >>> get_incidents_by_district("Vest")
        >>> get_incidents_by_district("SørØst")
        
    Returns:
        list[dict]: A list of dictionaries containing the incidents.
    """
    url = f"https://api.politiet.no/politiloggen/v1/messages?Districts={district_name}"
    headers = {"accept": "application/json"}
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return [{"error": "Failed to fetch incidents due to HTTP error", "details": str(e)}]
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
        return [{"error": "Failed to fetch incidents due to request error", "details": str(e)}]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [{"error": "An unexpected error occurred", "details": str(e)}]


@mcp.tool()
def get_incidents_by_municipality(municipality_name: str) -> list[dict]:
    """Fetches incidents from the Norwegian Police API filtered by a specific municipality.
    
    Args:
        municipality_name (str): The name of the municipality to filter by.
        
    Returns:
        list[dict]: A list of dictionaries containing the incidents.
    """
    url = f"https://api.politiet.no/politiloggen/v1/messages?Municipalities={municipality_name}"
    headers = {"accept": "application/json"}
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return [{"error": "Failed to fetch incidents due to HTTP error", "details": str(e)}]
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
        return [{"error": "Failed to fetch incidents due to request error", "details": str(e)}]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [{"error": "An unexpected error occurred", "details": str(e)}]


@mcp.tool()
def search_stock_ticker(company_name: str) -> dict:
    """Searches for the stock ticker of a company using the Alpha Vantage API.

    Args:
        company_name (str): The name of the company to search for.

    Returns:
        dict: A dictionary containing the search results or an error message.
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")  # Replace with your actual Alpha Vantage API key
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}"
    headers = {"accept": "application/json"}
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return {"error": "Failed to search stock ticker due to HTTP error", "details": str(e)}
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
        return {"error": "Failed to search stock ticker due to request error", "details": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred while searching stock ticker", "details": str(e)}


@mcp.tool()
def get_stock_price(symbol: str) -> dict:
    """Gets the current price of a stock using its ticker symbol from the Alpha Vantage API.

    Args:
        symbol (str): The stock ticker symbol.

    Returns:
        dict: A dictionary containing the stock price information or an error message.
    """
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")  # Replace with your actual Alpha Vantage API key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    headers = {"accept": "application/json"}
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # The API returns time series data; we'll extract the latest available price.
        # The structure is "Time Series (Daily)": { "YYYY-MM-DD": { "1. open": "...", "4. close": "..." } }
        time_series = data.get("Time Series (Daily)")
        if not time_series:
            return {"error": "No time series data found for the symbol", "details": data}
        
        # Get the latest date (first key in the time_series dictionary)
        latest_date = next(iter(time_series))
        latest_data = time_series[latest_date]
        return {
            "symbol": symbol,
            "date": latest_date,
            "open": latest_data.get("1. open"),
            "high": latest_data.get("2. high"),
            "low": latest_data.get("3. low"),
            "close": latest_data.get("4. close"),
            "volume": latest_data.get("5. volume")
        }
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return {"error": "Failed to get stock price due to HTTP error", "details": str(e)}
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
        return {"error": "Failed to get stock price due to request error", "details": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred while getting stock price", "details": str(e)}


def main():
    """Runs the MCP server."""
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main() 