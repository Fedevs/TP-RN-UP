# Sistema multiagente de subastas

TP integrador de Redes Neuronales. El usuario escribe en lenguaje natural (ej. *"Quiero subastar mi PS5, ¿a cuánto la pongo?"*) y cuatro agentes coordinados con **LangGraph** y **Gemini** le arman la subasta:

| Agente | Qué hace |
|--------|----------|
| **Coordinador** | Entiende qué quiere el usuario y extrae los datos del producto |
| **Analista** | Busca subastas similares en la base de datos y sugiere un precio |
| **Subastas** | Redacta el título y la descripción de la publicación |
| **Validador** | Revisa que la publicación cumpla los requisitos; si no, vuelve a Subastas |

El diseño completo y el diagrama están en [docs/diagrama.md](docs/diagrama.md).

## Instalación

Requiere **Python 3.11 o superior**.

```powershell
git clone https://github.com/Fedevs/TP-RN-UP.git
cd TP-RN-UP

python -m venv .venv
.venv\Scripts\Activate.ps1        # en Mac/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

Después:

1. Copiá `.env.example` como `.env` y completá tu API key de Gemini (se saca gratis en [Google AI Studio](https://aistudio.google.com/apikey)).
2. Creá la base de datos de productos:
   ```powershell
   python data/create_db.py
   ```

## Uso

Desde la carpeta `src`, con el entorno virtual activado:

```powershell
cd src
python main.py "Quiero subastar mi PS5 con 2 joysticks, ¿a cuánto la pongo?"   # un mensaje
python main.py                                                                 # conversación ("salir" para terminar)
```

Se muestra cada paso del grafo (qué agente se ejecutó y qué devolvió) y al final la respuesta.

Cada agente también se puede probar solo, por ejemplo: `python -m agents.coordinator`.

> **Ojo con la cuota gratuita de Gemini:** permite pocos pedidos por minuto y por día, y crear una subasta usa unos 4. Si aparece `429 RESOURCE_EXHAUSTED`, esperá un minuto. Podés ver tu cuota en https://ai.dev/rate-limit.

## Estructura

```
data/create_db.py      Crea la base SQLite con subastas de referencia
docs/diagrama.md       Diseño: agentes, estado compartido y diagrama
src/main.py            Punto de entrada
src/graph.py           Grafo de LangGraph: nodos, aristas y routers
src/state.py           Estado compartido entre agentes
src/agents/            Un archivo por agente
src/llm.py             Configuración del modelo Gemini
src/tools.py, db.py    Búsqueda de productos similares en la base
```
