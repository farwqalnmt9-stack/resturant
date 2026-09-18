"""Local MCP server for managing this restaurant's Django orders.

Run from the project folder with the project's virtual environment:
    .venv\\Scripts\\python.exe restaurant_mcp.py
"""

import os
from datetime import date
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from mcp.server import MCPServer
from orders.models import Order


mcp = MCPServer("Restaurant Operations")


def _money(value: Decimal | None) -> str:
    return f"{value or Decimal('0'):.2f} ل.س"


def _order_summary(order: Order, include_private: bool = False) -> dict:
    data = {
        "order_number": order.order_number,
        "status": order.get_status_display(),
        "status_code": order.status,
        "total": _money(order.total),
        "created_at": order.created_at.isoformat(),
        "delivery_person": order.delivery_person.get_username() if order.delivery_person else None,
    }
    if include_private:
        data.update({
            "phone": order.phone,
            "address": order.address,
            "delivery_coordinates": [str(order.delivery_latitude), str(order.delivery_longitude)] if order.delivery_latitude is not None else None,
            "items": [
                {"name": item.product_name, "quantity": item.quantity, "notes": item.notes, "line_total": _money(item.line_total)}
                for item in order.items.all()
            ],
        })
    return data


@mcp.tool()
def list_orders(status: str | None = None, limit: int = 20) -> list[dict]:
    """List recent orders. Optionally filter by a status code such as pending or preparing."""
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    valid_statuses = {choice for choice, _ in Order.Status.choices}
    if status and status not in valid_statuses:
        raise ValueError(f"Unknown status. Use one of: {', '.join(sorted(valid_statuses))}")
    orders = Order.objects.select_related("delivery_person").order_by("-created_at")
    if status:
        orders = orders.filter(status=status)
    return [_order_summary(order) for order in orders[:limit]]


@mcp.tool()
def get_order(order_number: str) -> dict:
    """Return one order with its customer delivery details and items."""
    order = Order.objects.select_related("delivery_person").prefetch_related("items").filter(order_number=order_number.upper()).first()
    if not order:
        raise ValueError("Order not found")
    return _order_summary(order, include_private=True)


@mcp.tool()
def update_order_status(order_number: str, status: str) -> dict:
    """Update an order status. Valid values: pending, confirmed, preparing, ready, out, delivered, cancelled."""
    valid_statuses = {choice for choice, _ in Order.Status.choices}
    if status not in valid_statuses:
        raise ValueError(f"Unknown status. Use one of: {', '.join(sorted(valid_statuses))}")
    order = Order.objects.filter(order_number=order_number.upper()).first()
    if not order:
        raise ValueError("Order not found")
    order.status = status
    order.save(update_fields=["status", "updated_at"])
    return _order_summary(order)


@mcp.tool()
def assign_delivery_person(order_number: str, username: str) -> dict:
    """Assign a delivery person to an order using their Django username."""
    order = Order.objects.filter(order_number=order_number.upper()).first()
    if not order:
        raise ValueError("Order not found")
    user = get_user_model().objects.filter(username=username).first()
    if not user:
        raise ValueError("Delivery person not found")
    order.delivery_person = user
    order.save(update_fields=["delivery_person", "updated_at"])
    return _order_summary(order)


@mcp.tool()
def daily_sales(for_date: str | None = None) -> dict:
    """Return completed-order revenue for a date in YYYY-MM-DD format; defaults to today."""
    try:
        target_date = date.fromisoformat(for_date) if for_date else timezone.localdate()
    except ValueError as error:
        raise ValueError("for_date must use YYYY-MM-DD") from error
    completed = Order.objects.filter(status=Order.Status.DELIVERED, created_at__date=target_date)
    total = completed.aggregate(total=Sum("total"))["total"]
    return {"date": target_date.isoformat(), "completed_orders": completed.count(), "revenue": _money(total)}


if __name__ == "__main__":
    mcp.run()
