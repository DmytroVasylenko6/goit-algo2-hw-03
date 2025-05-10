import networkx as nx
import pandas as pd

# Створення орієнтованого графа
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додаємо всі ребра з пропускними здатностями до графа
for u, v, capacity in edges:
    G.add_edge(u, v, capacity=capacity)

# Додаємо супер-джерело та супер-сток для моделювання потоків
G.add_edge("Джерело", "Термінал 1", capacity=float("inf"))
G.add_edge("Джерело", "Термінал 2", capacity=float("inf"))

for i in range(1, 15):
    G.add_edge(f"Магазин {i}", "Сток", capacity=float("inf"))

# Розрахунок максимального потоку за алгоритмом Едмондса-Карпа
flow_value, flow_dict = nx.maximum_flow(
    G, "Джерело", "Сток", flow_func=nx.algorithms.flow.edmonds_karp
)

print(f"Максимальний потік: {flow_value} одиниць")

# Додаємо виведення потоків через Склад 1
print("\nПотоки через Склад 1:")
for shop in G["Склад 1"]:
    if shop.startswith("Магазин"):
        flow = flow_dict["Склад 1"].get(shop, 0)
        print(f"Склад 1 -> {shop}: {flow} одиниць")

# Додаємо виведення потоків через Склад 2
print("\nПотоки через Склад 2:")
for shop in G["Склад 2"]:
    if shop.startswith("Магазин"):
        flow = flow_dict["Склад 2"].get(shop, 0)
        print(f"Склад 2 -> {shop}: {flow} одиниць")

# Додаємо виведення потоків через Склад 3
print("\nПотоки через Склад 3:")
for shop in G["Склад 3"]:
    if shop.startswith("Магазин"):
        flow = flow_dict["Склад 3"].get(shop, 0)
        print(f"Склад 3 -> {shop}: {flow} одиниць")

# Додаємо виведення потоків через Склад 4
print("\nПотоки через Склад 4:")
for shop in G["Склад 4"]:
    if shop.startswith("Магазин"):
        flow = flow_dict["Склад 4"].get(shop, 0)
        print(f"Склад 4 -> {shop}: {flow} одиниць")

# Формуємо таблицю результатів
results = []
for terminal in ["Термінал 1", "Термінал 2"]:
    for warehouse in G[terminal]:
        for shop in G[warehouse]:
            if shop.startswith("Магазин"):
                flow = flow_dict[terminal].get(warehouse, 0)
                warehouse_flow = flow_dict[warehouse].get(shop, 0)
                if warehouse_flow > 0:
                    results.append(
                        {
                            "Термінал": terminal,
                            "Магазин": shop,
                            "Фактичний Потік (одиниць)": warehouse_flow,
                        }
                    )

df = pd.DataFrame(results)
print(df.to_string(index=False))
