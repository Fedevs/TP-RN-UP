import statistics

from db import connect


def search_similar(category, keywords):
    """Devuelve los productos de una categoría cuyo nombre contiene al menos una de las keywords.

    Si keywords está vacía, devuelve todos los productos de la categoría.
    """
    query = "SELECT * FROM products WHERE category = ?"
    values = [category]

    if keywords:
        keyword_conditions = " OR ".join(["name LIKE ?"] * len(keywords))
        query += f" AND ({keyword_conditions})"
        values += [f"%{keyword}%" for keyword in keywords]

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(query, values)
    rows = cursor.fetchall()
    products = [dict(row) for row in rows]
    connection.close()

    return products


def price_stats(products):
    """Devuelve la cantidad, el mínimo, el máximo y la mediana de los precios finales.

    Devuelve None si la lista está vacía.
    """
    if not products:
        return None

    prices = [product["final_price"] for product in products]

    return {
        "count": len(prices),
        "min_price": min(prices),
        "max_price": max(prices),
        "median_price": round(statistics.median(prices)),
    }
