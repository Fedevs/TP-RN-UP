import statistics

from db import connect


def search_similar(category, keywords):
    """Returns the products of a category whose name contains at least one of the keywords.

    If keywords is empty, returns every product of the category.
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
    """Returns the count, min, max and median of the products' final prices.

    Returns None if the list is empty.
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
