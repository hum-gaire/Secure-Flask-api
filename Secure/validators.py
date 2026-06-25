import re

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 30:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None

def validate_password(password):
    return password and len(password) >= 8

def validate_order_data(data):
    if not isinstance(data, dict):
        return False, "Invalid data format"
    
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    
    if not isinstance(product_id, int) or product_id <= 0:
        return False, "Invalid product_id"
    if not isinstance(quantity, int) or quantity <= 0 or quantity > 100:
        return False, "Invalid quantity"
    
    return True, None
