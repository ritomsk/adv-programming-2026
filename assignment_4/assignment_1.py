products = [
    {"name": "USB Hub", "stock": 15},
    {"name": "Mouse", "stock": 10},
    {"name": "Keyboard", "stock": 7},
    {"name": "Joystick", "stock": 20},
    {"name": "Modem", "stock": 5},
]

print("Products with stock less than 10 are: ")

for product in products:
    if product["stock"] < 10:
        print(f"Product: {product['name']}, Stock: {product['stock']}")