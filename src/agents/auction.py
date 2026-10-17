import json
import sys

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from llm import llm
from state import State

DEFAULT_DURATION_DAYS = 7


class AuctionOutput(BaseModel):
    title: str = Field(
        description="Título de la publicación, entre 10 y 80 caracteres. Producto, modelo y lo más importante."
    )
    description: str = Field(
        description="Descripción de la publicación, entre 50 y 1000 caracteres. Clara y atractiva, "
        "usando solo los datos que dio el usuario."
    )


SYSTEM_PROMPT = """Sos el redactor de publicaciones de un sistema de subastas.
A partir de los datos del producto, escribí el título y la descripción de la subasta.

Reglas:
- Usá SOLO los datos que dio el usuario. Nunca inventes características, accesorios ni estado
  (ej. no digas "con caja original" si el usuario no lo dijo).
- El título tiene entre 10 y 80 caracteres.
- La descripción tiene entre 50 y 1000 caracteres.
- No menciones el precio: el sistema lo agrega aparte.
- Escribí en español rioplatense, como si fueras el vendedor publicando su producto.
- No menciones "los datos", "el sistema" ni nada del funcionamiento interno: el comprador no lo ve.

Si te pasan un borrador anterior con problemas, corregí esos problemas manteniendo lo que estaba bien."""

structured_llm = llm.with_structured_output(AuctionOutput)


def choose_starting_price(state):
    if state.get("user_price"):
        return state["user_price"]

    analysis = state.get("analysis") or {}
    if analysis.get("suggested_price"):
        return analysis["suggested_price"]

    raise ValueError("Auction agent needs a price: neither user_price nor suggested_price is set")


def auction(state: State) -> dict:
    product = state["product"]
    starting_price = choose_starting_price(state)

    user_message = f"Producto:\n{json.dumps(product, ensure_ascii=False, indent=2)}"

    validation = state.get("validation")
    if validation and not validation["approved"]:
        user_message += (
            f"\n\nBorrador anterior:\n{json.dumps(state['draft'], ensure_ascii=False, indent=2)}"
            f"\n\nProblemas a corregir:\n- " + "\n- ".join(validation["issues"])
        )

    result = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ])

    draft = {
        "title": result.title,
        "description": result.description,
        "category": product["category"],
        "starting_price": starting_price,
        "duration_days": DEFAULT_DURATION_DAYS,
    }

    return {"draft": draft, "retries": state.get("retries", 0) + 1}