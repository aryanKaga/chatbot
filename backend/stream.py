import asyncio
from langchain.callbacks.base import BaseCallbackHandler

class StreamingPrintHandler(BaseCallbackHandler):
    def __init__(self):
        self.queue = asyncio.Queue()
        self.closed = False

    async def on_llm_new_token(self, token: str, **kwargs):
        await self.queue.put(token)

    async def aclose(self):
        self.closed = True
        await self.queue.put(None)

async def event_stream(handler: StreamingPrintHandler):
    while True:
        token = await handler.queue.get()
        if token is None:
            break
        yield f"{token}\n\n"