import asyncio
import logging
from typing import Callable, Coroutine, Any, Set

logger = logging.getLogger(__name__)

# Store active background tasks to prevent garbage collection
background_tasks: Set[asyncio.Task] = set()

def create_background_task(coro: Coroutine) -> asyncio.Task:
    """
    Create a background task and add it to the set of running tasks.
    
    Args:
        coro: The coroutine to run in the background
        
    Returns:
        The created task
    """
    task = asyncio.create_task(coro)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    
    logger.info(f"Background task created: {coro.__qualname__ if hasattr(coro, '__qualname__') else 'Unknown'}")
    
    return task