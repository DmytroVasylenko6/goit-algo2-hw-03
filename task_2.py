import timeit

import pandas as pd
from BTrees.OOBTree import OOBTree


def load_data_from_csv(filepath):
    df = pd.read_csv(filepath)
    items = df.to_dict(orient="records")
    return items


id_tree = OOBTree()  # За ID
price_tree = OOBTree()  # За Price
dct = {}  # Стандартний словник


def add_item_to_dict(dct, item):
    dct[item["ID"]] = {
        "ID": item["ID"],
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": float(item["Price"]),
    }


def add_item_to_trees(id_tree, price_tree, item):
    item_data = {
        "ID": item["ID"],
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": float(item["Price"]),
    }
    id_tree[item["ID"]] = item_data

    price = item_data["Price"]
    if price in price_tree:
        price_tree[price].append(item_data)
    else:
        price_tree[price] = [item_data]


def range_query_dict(dct, min_price, max_price):
    return [item for item in dct.values() if min_price <= item["Price"] <= max_price]


def range_query_id_tree(id_tree, min_price, max_price):
    return [
        item for item in id_tree.values() if min_price <= item["Price"] <= max_price
    ]


def range_query_price_tree(price_tree, min_price, max_price):
    result = []
    for _, items in price_tree.items(min_price, max_price):
        result.extend(items)
    return result


def main():
    filepath = "generated_items_data.csv"
    items = load_data_from_csv(filepath)

    for item in items:
        add_item_to_dict(dct, item)
        add_item_to_trees(id_tree, price_tree, item)

    setup_dict = (
        "from __main__ import range_query_dict, dct\n"
        "min_price, max_price = 10.0, 100.0"
    )

    setup_id_tree = (
        "from __main__ import range_query_id_tree, id_tree\n"
        "min_price, max_price = 10.0, 100.0"
    )

    setup_price_tree = (
        "from __main__ import range_query_price_tree, price_tree\n"
        "min_price, max_price = 10.0, 100.0"
    )

    time_dict = timeit.timeit(
        "range_query_dict(dct, min_price, max_price)", setup=setup_dict, number=100
    )
    time_id_tree = timeit.timeit(
        "range_query_id_tree(id_tree, min_price, max_price)",
        setup=setup_id_tree,
        number=100,
    )
    time_price_tree = timeit.timeit(
        "range_query_price_tree(price_tree, min_price, max_price)",
        setup=setup_price_tree,
        number=100,
    )

    print(f"Total range_query time for Dict: {time_dict:.6f} seconds")
    print(f"Total range_query time for OOBTree (ID): {time_id_tree:.6f} seconds")
    print(f"Total range_query time for Price-OOBTree: {time_price_tree:.6f} seconds")


if __name__ == "__main__":
    main()
