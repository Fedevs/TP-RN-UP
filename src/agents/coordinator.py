from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from llm import llm
from state import State

Intent = Literal[
    "create_auction_no_price",
    "create_auction_with_price",
    "price_query",
    "missing_info",
    "off_topic",
]
Category = Literal["consoles", "phones", "laptops", "tvs", "bicycles", "other"]
Condition = Literal["new", "used", "refurbished"]


class Product(BaseModel):
    name: str = Field(
        description="Nombre comercial completo del producto, con marca y modelo. "
        "Usar el nombre oficial y no abreviaturas (ej. 'PS5' -> 'PlayStation 5')."
    )
    category: Category = Field(description="Categoría del producto. Si no encaja en ninguna, 'other'.")
    condition: Condition | None = Field(description="Estado del producto, solo si el usuario lo dice.")
    details: str | None = Field(
        description="Otros detalles que dio el usuario (accesorios, uso, defectos). No inventar nada."
    )


class CoordinatorOutput(BaseModel):
    intent: Intent
    product: Product | None = Field(description="El producto. null en missing_info y off_topic.")
    user_price: int | None = Field(
        description="Precio que pide el usuario, en pesos enteros, solo si lo dice explícitamente "
        "(ej. '500 lucas' -> 500000). Si no dice un precio, null."
    )
    response: str | None = Field(
        description="Solo en missing_info y off_topic: respuesta breve y amable para el usuario. Si es off_topic, indicar " \
        "solo respondés a cuestiones de subastas."
        "En el resto de los casos, null."
    )


SYSTEM_PROMPT = """Sos el coordinador de un sistema de subastas.
Tu tarea es entender qué quiere el usuario y extraer los datos del producto.

Clasificá el mensaje en una de estas intenciones:
- create_auction_no_price: quiere subastar un producto y NO dice a qué precio (aunque pregunte cuánto pedir).
- create_auction_with_price: quiere subastar un producto y dice a qué precio.
- price_query: solo quiere saber cuánto vale un producto, sin intención de subastarlo.
- missing_info: quiere subastar algo pero no dice qué producto.
- off_topic: el mensaje no tiene que ver con subastas ni con precios.

Nunca inventes datos que el usuario no dio."""

structured_llm = llm.with_structured_output(CoordinatorOutput)


def coordinator(state: State) -> dict:
    result = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["message"]),
    ])

    return {
        "intent": result.intent,
        "product": result.product.model_dump() if result.product else None,
        "user_price": result.user_price,
        "response": result.response,
    }
