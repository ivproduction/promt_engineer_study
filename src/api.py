"""FastAPI application for PsychoAI.

Простой пример FastAPI-приложения, которое будет
работать параллельно с Telegram-поллингом.
"""

from __future__ import annotations

import asyncio
import time
import uuid

from fastapi import FastAPI
from loguru import logger


app = FastAPI(title="PsychoAI API")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health-check endpoint."""
    return {"status": "ok"}


@app.get("/hello")
async def hello() -> dict[str, str | float]:
    """
    Демонстрационный endpoint.

    Спит 5 секунд (await asyncio.sleep(5)).
    При параллельных запросах все должны завершиться ~одновременно (~5 с),
    а не по очереди (20 с за 4 запроса).
    """
    req_id = uuid.uuid4().hex[:8]
    t0 = time.perf_counter()
    logger.info(f"[{req_id}] /hello START")
    await asyncio.sleep(5)
    elapsed = time.perf_counter() - t0
    logger.info(f"[{req_id}] /hello DONE in {elapsed:.2f}s")
    return {"message": "Hello, world!", "req_id": req_id, "elapsed_sec": round(elapsed, 2)}


@app.get("/hello_busy")
async def hello_busy() -> dict[str, str | float]:
    """
    Спит 5 секунд в потоке (asyncio.to_thread(time.sleep, 5)).

    Занимает один воркер из пула (~14 на M1 Max). При 200 запросах
    они обрабатываются «пачками» по ~14 → общее время ~ (200/14)*5 ≈ 70+ с.
    """
    req_id = uuid.uuid4().hex[:8]
    t0 = time.perf_counter()
    logger.info(f"[{req_id}] /hello_busy START")
    await asyncio.to_thread(time.sleep, 5)
    elapsed = time.perf_counter() - t0
    logger.info(f"[{req_id}] /hello_busy DONE in {elapsed:.2f}s")
    return {"message": "Hello, world!", "req_id": req_id, "elapsed_sec": round(elapsed, 2)}

