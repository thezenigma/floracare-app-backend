import asyncio
import logging

logger = logging.getLogger(__name__)

class RateLimitedQueue:
    def __init__(self, requests_per_minute: int = 40):
        self.queue = asyncio.Queue()
        self.delay = 60.0 / requests_per_minute
        self._worker_task = None

    def start(self):
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._worker())

    async def _worker(self):
        while True:
            func, args, kwargs, future = await self.queue.get()
            try:
                result = await func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                logger.error(f"Error in queued task: {e}")
                future.set_exception(e)
            finally:
                self.queue.task_done()
                # Enforce the strict rate limit delay after processing each task
                await asyncio.sleep(self.delay)

    async def enqueue(self, func, *args, **kwargs):
        future = asyncio.Future()
        await self.queue.put((func, args, kwargs, future))
        return await future

# Singleton instance for the app
agent_queue = RateLimitedQueue(requests_per_minute=40)
