#!/usr/bin/env python3
"""MCP server — KB universitaria di Stek. Si collega a Claude Code via stdio."""

import os
import sys
import asyncio

KB_PATH  = os.path.expanduser("~/Desktop/Magistrale/_KB")
DB_PATH  = os.path.join(KB_PATH, ".chromadb")
MODEL    = "paraphrase-multilingual-MiniLM-L12-v2"

# Usa il venv dedicato senza attivarlo
VENV_SITE = os.path.join(KB_PATH, ".venv/lib/python3.12/site-packages")
sys.path.insert(0, VENV_SITE)

import chromadb
from sentence_transformers import SentenceTransformer
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("kb-universitaria")

_model: SentenceTransformer | None = None
_col = None

def _get():
    global _model, _col
    if _model is None:
        _model = SentenceTransformer(MODEL)
    if _col is None:
        client = chromadb.PersistentClient(path=DB_PATH)
        _col = client.get_or_create_collection("kb-notes")
    return _model, _col


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_kb",
            description=(
                "Cerca nella knowledge base universitaria di Stek (appunti di lezioni, "
                "concetti, definizioni). Usa questo tool OGNI VOLTA che l'utente fa una "
                "domanda su argomenti del corso o chiede di spiegare qualcosa che potrebbe "
                "essere nelle sue note."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Concetto, domanda o parola chiave da cercare negli appunti"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Numero di risultati (default 6)",
                        "default": 6
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name != "search_kb":
        return [TextContent(type="text", text=f"Tool sconosciuto: {name}")]

    query = arguments["query"]
    n     = int(arguments.get("n", 6))

    try:
        model, col = _get()
    except Exception as e:
        return [TextContent(type="text", text=f"KB non ancora indicizzata. Errore: {e}")]

    try:
        results = col.query(
            query_embeddings=model.encode([query]).tolist(),
            n_results=n
        )
    except Exception as e:
        return [TextContent(type="text", text=f"Errore query: {e}")]

    docs      = results["documents"][0]
    metas     = results["metadatas"][0]
    distances = results["distances"][0]

    if not docs:
        return [TextContent(type="text", text="Nessun risultato trovato nella KB.")]

    parts = []
    for doc, meta, dist in zip(docs, metas, distances):
        rel   = os.path.relpath(meta["file"], KB_PATH)
        score = round((1 - dist) * 100, 1)
        parts.append(f"[{score}% — {rel}]\n{doc.strip()}")

    return [TextContent(type="text", text="\n\n---\n\n".join(parts))]


async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
