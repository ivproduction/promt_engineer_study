"""
OpenAI Assistants API Example with Threads.

This demonstrates the basic flow:
1. Create an Assistant (or use existing)
2. Create a Thread (conversation)
3. Add a Message to the Thread
4. Run the Assistant on the Thread
5. Poll for completion and get the response
"""

import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

# Load environment variables
load_dotenv()


def create_assistant(client: OpenAI) -> str:
    """Create a simple assistant and return its ID."""
    assistant = client.beta.assistants.create(
        name="PsychoAI Demo",
        instructions="""You are a helpful and empathetic assistant. 
        You listen carefully and provide thoughtful responses.
        Keep responses concise but warm.""",
        model="gpt-4o-mini",
    )
    logger.info(f"Created assistant: {assistant.id}")
    return assistant.id


def run_conversation(client: OpenAI, assistant_id: str, user_message: str) -> str:
    """
    Run a single conversation turn with the assistant.
    
    Args:
        client: OpenAI client
        assistant_id: ID of the assistant to use
        user_message: User's input message
        
    Returns:
        Assistant's response text
    """
    # 1. Create a Thread
    thread = client.beta.threads.create()
    logger.info(f"Created thread: {thread.id}")
    
    # 2. Add user message to the Thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )
    logger.info(f"Added message: {user_message[:50]}...")
    
    # 3. Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    logger.info(f"Started run: {run.id}")
    
    # 4. Poll for completion
    while run.status in ["queued", "in_progress"]:
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        logger.debug(f"Run status: {run.status}")
    
    if run.status != "completed":
        logger.error(f"Run failed with status: {run.status}")
        return f"Error: Run ended with status {run.status}"
    
    # 5. Get the response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    # Get the last assistant message
    for message in messages.data:
        if message.role == "assistant":
            response_text = message.content[0].text.value
            logger.info(f"Got response: {response_text[:50]}...")
            return response_text
    
    return "No response from assistant"


def main() -> None:
    """Main entry point."""
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment")
        print("❌ Please add OPENAI_API_KEY to your .env file")
        return
    
    # Initialize client
    client = OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized")
    
    # Create assistant (in production, you'd save and reuse the ID)
    assistant_id = create_assistant(client)
    
    # Example conversation
    user_input = "Привет! Расскажи, как ты можешь помочь мне?"
    
    print(f"\n👤 User: {user_input}\n")
    
    response = run_conversation(client, assistant_id, user_input)
    
    print(f"🤖 Assistant: {response}\n")
    
    # Cleanup: delete the assistant (optional, for demo purposes)
    client.beta.assistants.delete(assistant_id)
    logger.info(f"Deleted assistant: {assistant_id}")


if __name__ == "__main__":
    main()
