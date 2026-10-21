import csv, os, random

random.seed(42)
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample')
os.makedirs(SAMPLE_DIR, exist_ok=True)

# 1. Departments
departments = [
    (1, "Produce"),
    (2, "Dairy Eggs"),
    (3, "Bakery"),
    (4, "Beverages"),
    (5, "Snacks"),
    (6, "Pantry"),
    (7, "Frozen"),
    (8, "Personal Care")
]
with open(os.path.join(SAMPLE_DIR, 'departments.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['department_id', 'department'])
    w.writerows(departments)

# 2. Products
products = [
    (1, "Organic Bananas", 1, 1, 0.82),
    (2, "Bag of Organic Bananas", 1, 1, 0.78),
    (3, "Organic Strawberries", 1, 1, 0.71),
    (4, "Organic Baby Spinach", 1, 1, 0.65),
    (5, "Hass Avocados", 1, 1, 0.68),
    (6, "Whole Milk 1 Gallon", 2, 2, 0.79),
    (7, "Large Grade A Eggs 12ct", 2, 2, 0.74),
    (8, "Organic Greek Plain Yogurt", 2, 2, 0.62),
    (9, "Unsalted Butter 16oz", 2, 2, 0.58),
    (10, "Cheddar Cheese Block", 2, 2, 0.51),
    (11, "Whole Wheat Bread", 3, 3, 0.69),
    (12, "Sourdough Boule", 3, 3, 0.45),
    (13, "Butter Croissant 4pk", 3, 3, 0.40),
    (14, "Sparkling Water Lime 12pk", 4, 4, 0.72),
    (15, "100% Orange Juice 59oz", 4, 4, 0.60),
    (16, "Cold Brew Coffee 32oz", 4, 4, 0.66),
    (17, "Sea Salt Potato Chips", 5, 5, 0.54),
    (18, "Dark Chocolate Almonds", 5, 5, 0.48),
    (19, "Organic Tortilla Chips", 5, 5, 0.52),
    (20, "Extra Virgin Olive Oil 500ml", 6, 6, 0.35),
    (21, "Organic Pasta Spaghetti", 6, 6, 0.42),
    (22, "Tomato Basil Pasta Sauce", 6, 6, 0.46),
    (23, "Frozen Organic Blueberries", 7, 7, 0.49),
    (24, "Frozen Thin Crust Pizza", 7, 7, 0.43),
    (25, "Hand Sanitizer Citrus 8oz", 8, 8, 0.28)
]

with open(os.path.join(SAMPLE_DIR, 'products.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['product_id', 'product_name', 'aisle_id', 'department_id'])
    for p in products:
        w.writerow([p[0], p[1], p[2], p[3]])

# 3. Orders (250 orders across 45 users, 24 hours, 7 days)
orders = []
order_priors = []
order_trains = []

users = list(range(101, 150))
order_id = 1

# Weights for hours: peak 8am-11am & 4pm-8pm
hour_weights = [
    5, 3, 2, 1, 2, 4, 10, 18, 35, 55, 60, 52,
    48, 42, 38, 45, 58, 65, 70, 58, 40, 28, 15, 8
]
# Weights for day of week: peak Sunday(0) and Saturday(6)
dow_weights = [60, 45, 40, 38, 42, 52, 65]

for u in users:
    n_orders = random.randint(3, 8)
    for ord_num in range(1, n_orders + 1):
        hour = random.choices(range(24), weights=hour_weights)[0]
        dow = random.choices(range(7), weights=dow_weights)[0]
        days_since = "" if ord_num == 1 else random.randint(2, 14)
        orders.append((order_id, u, ord_num, dow, hour, days_since))
        
        # Pick 3 to 7 products for this basket
        basket_size = random.randint(3, 7)
        # Higher probability for top items
        prod_choices = random.sample(products, basket_size)
        
        for add_order, prod in enumerate(prod_choices, 1):
            is_reordered = 1 if (ord_num > 1 and random.random() < prod[4]) else 0
            row = (order_id, prod[0], add_order, is_reordered)
            if order_id % 5 == 0:
                order_trains.append(row)
            else:
                order_priors.append(row)
                
        order_id += 1

with open(os.path.join(SAMPLE_DIR, 'orders.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['order_id', 'user_id', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order'])
    w.writerows(orders)

with open(os.path.join(SAMPLE_DIR, 'order_products__prior.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['order_id', 'product_id', 'add_to_cart_order', 'reordered'])
    w.writerows(order_priors)

with open(os.path.join(SAMPLE_DIR, 'order_products__train.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['order_id', 'product_id', 'add_to_cart_order', 'reordered'])
    w.writerows(order_trains)

print(f"Generated {len(orders)} orders, {len(products)} products, {len(departments)} departments.")
