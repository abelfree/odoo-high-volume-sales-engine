import json
import random
import sys


def generate_orders(count=10000):
    items = []
    for i in range(1, count + 1):
        items.append({
            "external_ref": f"EXT-{i}",
            "partner_id": 1,
            "lines": [{"product_id": random.randint(1, 10), "qty": 1, "price_unit": 10}],
        })
    return items


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    print(json.dumps(generate_orders(count)))
