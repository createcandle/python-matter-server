import asyncio
import logging
import os
import sys
from pathlib import Path

from .matter_stack import MatterStack
from .server import MatterServer

logging.basicConfig(level=logging.WARN)
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


def main() -> int:
    host = os.getenv("CHIP_WS_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("CHIP_WS_SERVER_PORT", "8080"))
    storage_path = os.getenv(
        "CHIP_WS_STORAGE",
        str(Path.home() / ".chip-storage/python-kv.json"),
    )

    stack = MatterStack()
    stack.setup(storage_path)

    loop = asyncio.get_event_loop()

    async def create_server():
        return MatterServer(stack)

    server = loop.run_until_complete(create_server())
    server.run(host, port)
    stack.shutdown()


if __name__ == "__main__":
    sys.exit(main())