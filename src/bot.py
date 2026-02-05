"""PsychoAI Telegram Bot.

A Telegram bot for psychotherapists that provides AI-powered analysis
and support using OpenAI Assistants API.
"""

import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from loguru import logger

from src.config import TELEGRAM_BOT_TOKEN
from src.assistant import PsychoAIAssistant


# Global assistant instance
assistant: PsychoAIAssistant | None = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")
    
    welcome_message = f"""👋 Привет, {user.first_name}!

Я **PsychoAI** — интеллектуальный ассистент для психотерапевтов.

🧠 **Что я умею:**
• Анализировать речевые паттерны клиентов
• Предлагать терапевтические интервенции
• Выявлять потенциальные риски (⚠️ Red Shield)

📝 **Как использовать:**
Просто напишите описание ситуации или запрос клиента — я дам анализ и рекомендации.

⚡ **Команды:**
/start — начать заново
/reset — очистить историю диалога
/help — справка

⚠️ **Важно:** Я НЕ заменяю профессиональную экспертизу. Используйте меня как инструмент поддержки.

Готов к работе! Опишите ситуацию."""

    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reset command - clear conversation history."""
    user_id = update.effective_user.id
    
    if assistant:
        assistant.reset_thread(user_id)
    
    await update.message.reply_text(
        "🔄 История диалога очищена. Начинаем с чистого листа!"
    )
    logger.info(f"User {user_id} reset conversation")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = """📚 **Справка PsychoAI**

**Примеры запросов:**

1️⃣ *Простой анализ:*
"Клиент говорит, что чувствует себя одиноким последние месяцы"

2️⃣ *Выявление паттернов:*
"Клиент в третий раз упоминает конфликт с матерью. Что это может значить?"

3️⃣ *Кризисная ситуация:*
"Клиент сказал: я больше не хочу просыпаться"

**Функции безопасности:**
⚠️ При обнаружении маркеров риска я выдам ALERT с рекомендациями.

**Команды:**
/start — приветствие
/reset — новый диалог
/help — эта справка"""

    await update.message.reply_text(help_text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user = update.effective_user
    user_message = update.message.text
    
    logger.info(f"Message from {user.id}: {user_message[:50]}...")
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    try:
        # Get response from assistant
        response = await assistant.chat(user.id, user_message)
        
        # Send response (split if too long)
        if len(response) > 4096:
            for i in range(0, len(response), 4096):
                await update.message.reply_text(response[i:i+4096])
        else:
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке запроса. Попробуйте позже."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Run the bot."""
    global assistant
    
    # Validate config
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found!")
        print("❌ Добавьте TELEGRAM_BOT_TOKEN в .env файл")
        return
    
    # Initialize assistant
    logger.info("Initializing PsychoAI assistant...")
    assistant = PsychoAIAssistant()
    assistant.create_assistant()
    
    # Build application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handler
    app.add_error_handler(error_handler)
    
    # Run bot
    logger.info("🚀 PsychoAI bot is starting...")
    print("🤖 PsychoAI бот запущен! Нажмите Ctrl+C для остановки.")
    
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    finally:
        # Cleanup
        if assistant:
            assistant.cleanup()
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()
