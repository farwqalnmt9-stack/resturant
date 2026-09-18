# Restaurant Operations MCP

This local MCP server gives an AI assistant controlled access to restaurant operations. It runs on the same computer as the Django project and uses the existing database.

## Available tools

- `list_orders` — recent orders, optionally filtered by status.
- `get_order` — one order with its delivery details and items.
- `update_order_status` — changes an order status.
- `assign_delivery_person` — assigns a Django user as the delivery person.
- `daily_sales` — reports revenue from delivered orders for a chosen date.

## Installation and local run

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\restaurant_mcp.py
```

The server uses the standard input/output MCP transport. Keep it local and only connect it to an assistant you trust: the tools can read customer delivery information and update orders.
