from fastmcp import FastMCP
from data import AIRLINE_FAQ

mcp = FastMCP("Nazwa Serwera")



@mcp.tool
def airline_faq(topic: str) -> dict:
   """
    Get an answer to a frequently asked question about airlines.
   """
   topic = topic.lower().strip()

   return AIRLINE_FAQ.get(topic, {"answer": "Nie znaleziono odpowiedzi na to pytanie.", "category": "other"})


@mcp.tool
def add(a: float, b: float) -> float:
   """
   Adds two numbers together.

   Args:
       a (float): The first number.
       b (float): The second number.

   Returns:
       float: The sum of the two numbers.
   """
   return a + b

@mcp.tool
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers together.
    
    Args:
         a (float): The first number.
         b (float): The second number.
    
    Returns:
         float: The product of the two numbers.
    """
    return a * b


if __name__ == "__main__":
   mcp.run(transport="http", port=8001)
