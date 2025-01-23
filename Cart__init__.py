import json
from products import Product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        # Use a static method for loading Cart data
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    # Retrieve cart details from the database
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Process and return the list of products directly
    products_list = []
    for cart_detail in cart_details:
        # Safely parse the contents, assuming contents is a JSON string
        try:
            contents = json.loads(cart_detail['contents'])
        except json.JSONDecodeError:
            continue  # Skip if contents are not valid JSON

        # Convert the content ids to actual product objects
        products_list.extend(products.get_product(content_id) for content_id in contents)

    return products_list


def add_to_cart(username: str, product_id: int):
    # Add the product to the user's cart
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    # Remove the product from the user's cart
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    # Delete the user's cart
    dao.delete_cart(username)
