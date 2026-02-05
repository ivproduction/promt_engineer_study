"""OpenAI Assistant integration for PsychoAI."""

import time
from openai import OpenAI
from loguru import logger

from src.config import OPENAI_API_KEY, OPENAI_MODEL, PSYCHOAI_SYSTEM_PROMPT


class PsychoAIAssistant:
    """Wrapper for OpenAI Assistants API."""
    
    def __init__(self) -> None:
        """Initialize the assistant."""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.assistant_id: str | None = None
        self._threads: dict[int, str] = {}  # user_id -> thread_id
        
    def create_assistant(self) -> str:
        """Create PsychoAI assistant and return its ID."""
        assistant = self.client.beta.assistants.create(
            name="PsychoAI",
            instructions=PSYCHOAI_SYSTEM_PROMPT,
            model=OPENAI_MODEL,
        )
        self.assistant_id = assistant.id
        logger.info(f"Created PsychoAI assistant: {self.assistant_id}")
        return self.assistant_id
    
    def get_or_create_thread(self, user_id: int) -> str:
        """Get existing thread or create new one for user."""
        if user_id not in self._threads:
            thread = self.client.beta.threads.create()
            self._threads[user_id] = thread.id
            logger.info(f"Created thread for user {user_id}: {thread.id}")
        return self._threads[user_id]
    
    def reset_thread(self, user_id: int) -> None:
        """Reset conversation for user (new thread)."""
        if user_id in self._threads:
            del self._threads[user_id]
            logger.info(f"Reset thread for user {user_id}")
    
    async def chat(self, user_id: int, message: str) -> str:
        """
        Send message and get response from assistant.
        
        Args:
            user_id: Telegram user ID (for thread management)
            message: User's message
            
        Returns:
            Assistant's response text
        """
        if not self.assistant_id:
            self.create_assistant()
        
        thread_id = self.get_or_create_thread(user_id)
        
        # Add user message
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )
        logger.debug(f"User {user_id}: {message[:50]}...")
        
        # Run assistant
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )
        
        # Poll for completion
        while run.status in ["queued", "in_progress"]:
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
        
        if run.status != "completed":
            logger.error(f"Run failed: {run.status}")
            return f"❌ Ошибка: {run.status}. Попробуйте позже."
        
        # Get response
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        
        for msg in messages.data:
            if msg.role == "assistant":
                response = msg.content[0].text.value
                logger.debug(f"Assistant: {response[:50]}...")
                return response
        
        return "Не удалось получить ответ. Попробуйте ещё раз."
    
    def cleanup(self) -> None:
        """Delete assistant on shutdown."""
        if self.assistant_id:
            try:
                self.client.beta.assistants.delete(self.assistant_id)
                logger.info(f"Deleted assistant: {self.assistant_id}")
            except Exception as e:
                logger.error(f"Failed to delete assistant: {e}")
