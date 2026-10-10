from mcp.server.mcpserver import MCPServer
import shopping_list
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("Shopping List")

@mcp.tool()
def list_items() -> list[dict]:
    """List every item currently on the shopping list.

    Returns a list of objects with an 'id' and a 'name'. Call this first
    whenever you need an item's id, for example before deleting something.
    """
    return shopping_list.list_items()

@mcp.tool()
def add_item(name: str) -> dict:
    """Add one item to the shopping list.

    Args:
        name: The item to add, e.g. 'milk' or '2 litres of oat milk'.

    Returns the new item with its id. Add each item separately if the
    user mentions several. Fails if the item is already on the list.
    """
    try:
        return shopping_list.add_item(name)
    except ValueError as e:
        raise ToolError(str(e)) from e

@mcp.tool()
def delete_item(item_id: int) -> dict:
    """Delete an item from the shopping list by its id.

    Args:
        item_id: The numeric id of the item, as returned by list_items
            or add_item. Do not guess ids; call list_items if unsure.

    Fails with an error if no item has that id.
    """
    try:
        return shopping_list.delete_item(item_id)
    except ValueError as e:
        raise ToolError(str(e)) from e

if __name__ == "__main__":
    mcp.run()