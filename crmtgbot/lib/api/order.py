from lib.schemas.product import ProductSchema
from retailcrm import v5 as RetailClient


def create_order(
    client: RetailClient,
    products: list[ProductSchema],
    phone: int,
    fullname: str,
    nickname: str | None = None,
) -> bool:
    first_name, last_name = fullname.split()
    order_info = {
        "firstName": first_name,
        "lastName": last_name,
        "managerComment": nickname if nickname else "no telegram nickname",
        "phone": phone,
        "items": [
            {
                "offer": {
                    "id": product.offers[0]["id"],
                },
                "quantity": 1,
            }
            for product in products
        ],
    }
    result = client.order_create(order_info).get_response()
    success = result["success"]
    return success
