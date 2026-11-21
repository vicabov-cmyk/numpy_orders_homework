from pathlib import Path

import numpy as np

csv_path = Path(__file__).with_name("orders.csv")

order_dtype = np.dtype([
    ("order_id", int),
    ("customer", "U100"),
    ("city", "U50"),
    ("product", "U100"),
    ("quantity", int),
    ("unit_price", float),
    ("discount", float),
    ("is_paid", bool),
    ("is_delivered", bool),
])

orders = np.genfromtxt(
    csv_path,
    delimiter=",",
    skip_header=1,
    dtype=order_dtype,
    encoding="utf-8-sig",
    autostrip=True,
    ndmin=1,
)

print(orders[:100])

prices = orders["unit_price"]

print("\nЦіни за одиницю товару:")
with np.printoptions(threshold=prices.size):
    print(prices)

print(f"Мінімальна ціна: {prices.min():.2f} грн")
print(f"Максимальна ціна: {prices.max():.2f} грн")
print(f"Середня ціна: {prices.mean():.2f} грн")

summary_fields = [
    "order_id",
    "customer",
    "city",
    "quantity",
    "unit_price",
    "is_paid",
]

order_summary = orders[summary_fields].copy()

print("\nСкорочений масив замовлень:")
print(order_summary)

# Обчислюємо суму кожного замовлення з урахуванням знижки
totals = orders["quantity"] * orders["unit_price"] * (1 - orders["discount"] / 100)

# Пункт 5. Виводимо кожне замовлення окремим рядком
print("\nЗвіт по замовленнях:")

for order, total in zip(orders, totals):
    paid = "Так" if order["is_paid"] else "Ні"
    delivered = "Так" if order["is_delivered"] else "Ні"

    print(
        f"Замовлення №{order['order_id']} | "
        f"Покупець: {order['customer']} | "
        f"Місто: {order['city']} | "
        f"Товар: {order['product']} | "
        f"Кількість: {order['quantity']} | "
        f"Сума: {total:.2f} грн | "
        f"Оплачено: {paid} | Доставлено: {delivered}"
    )

# Пункт 6. Підбиваємо підсумки

unpaid = ~orders["is_paid"]

print("\nПідсумки:")
print(f"Загальна вартість усіх замовлень: {totals.sum():.2f} грн")
print(f"Кількість неоплачених замовлень: {unpaid.sum()}")
print(f"Загальна вартість неоплачених замовлень: {totals[unpaid].sum():.2f} грн")