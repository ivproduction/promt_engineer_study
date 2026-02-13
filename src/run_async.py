"""Run Telegram bot and FastAPI app together in one asyncio event loop.

Запускает:
- Telegram-поллинг (python-telegram-bot, async)
- FastAPI (uvicorn) на том же event loop

Команда запуска:

    python -m src.run_async
"""

from __future__ import annotations

import asyncio

from loguru import logger
from telegram import Update

import uvicorn

from src.api import app as fastapi_app  # noqa: F401  - используется в uvicorn по строке "src.api:app"
from src.bot import assistant, build_application


async def run_telegram() -> None:
    """Запуск Telegram-поллинга внутри существующего event loop."""
    application = build_application()

    logger.info("Starting Telegram polling (async mode)...")

    try:
        # Рекомендуемый паттерн из документации python-telegram-bot v20+
        async with application:
            await application.start()
            await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

            # Блокируемся, пока нас не остановят (Ctrl+C / отмена задачи)
            stop_event: asyncio.Event = asyncio.Event()
            await stop_event.wait()
    finally:
        if assistant:
            assistant.cleanup()
        logger.info("Telegram bot stopped")


async def run_fastapi() -> None:
    """Запуск FastAPI через uvicorn.Server в том же event loop."""
    config = uvicorn.Config(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
    server = uvicorn.Server(config)

    logger.info("Starting FastAPI server on http://0.0.0.0:8000 ...")
    await server.serve()


async def main() -> None:
    """Точка входа: запускаем Telegram и FastAPI параллельно."""
    # Если одна из задач упадёт с ошибкой — asyncio.gather выбросит исключение.
    await asyncio.gather(run_fastapi(), run_telegram())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down (KeyboardInterrupt)")

