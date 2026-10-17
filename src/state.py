from typing import TypedDict


class State(TypedDict, total=False):
    """Datos compartidos por todos los agentes durante una ejecución del grafo.

    Cada agente lee algunos campos y devuelve solo los campos que escribe
    (ver la tabla "Estado compartido" en docs/diagrama.md).
    """

    # Entrada
    message: str  # mensaje del usuario
    history: list[dict]  # mensajes anteriores: [{"role": "user" | "assistant", "content": str}]

    # Los escribe el Coordinador
    intent: str  # create_auction_no_price, create_auction_with_price, price_query, missing_info, off_topic
    product: dict | None  # name, category, condition, details
    user_price: int | None  # precio que pidió el usuario, si lo dijo

    # Lo escribe el Analista
    analysis: dict  # enough_data, suggested_price, min_price, max_price, comparables, reasoning...

    # Los escribe Subastas
    draft: dict  # title, description, category, starting_price, duration_days
    retries: int  # cuántos borradores se generaron

    # Lo escribe el Validador
    validation: dict  # approved, issues

    # Respuesta final para el usuario (Coordinador o Analista, cuando el flujo termina ahí)
    response: str | None
