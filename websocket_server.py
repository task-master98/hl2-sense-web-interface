import os
import asyncio
import websockets
import signal

CONNECTED_CLIENTS = set()

async def handler(websocket, path):
    CONNECTED_CLIENTS.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    # try:
    async for message in websocket:
        print(f"Received message: {message}")
        for client in CONNECTED_CLIENTS:
            if client != websocket and client.open:
                await client.send(message)
    # finally:
    #     CONNECTED_CLIENTS.remove(websocket)
    #     print(f"Client disconnected: {websocket.remote_address}")

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        print(f"WebSocket server started on :{port}")
        await stop

if __name__ == "__main__":
    asyncio.run(main())